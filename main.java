import java.io.*;
import java.math.BigInteger;
import java.util.*;

public class main {

    static final int SHIFT = 16;

    static class FastScanner {
        private final InputStream in = System.in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }

        long nextLong() throws IOException {
            int c;
            do {
                c = read();
            } while (c <= ' ');

            long sign = 1;
            if (c == '-') {
                sign = -1;
                c = read();
            }

            long res = 0;
            while (c > ' ') {
                res = res * 10 + (c - '0');
                c = read();
            }
            return res * sign;
        }

        int nextInt() throws IOException {
            return (int) nextLong();
        }
    }

    static class Interval {
        long l, r;
        int col;

        Interval(long l, long r, int col) {
            this.l = l;
            this.r = r;
            this.col = col;
        }

        long length() {
            return r - l + 1;
        }
    }

    static long overlap(Interval a, Interval b) {
        long l = Math.max(a.l, b.l);
        long r = Math.min(a.r, b.r);
        return Math.max(0L, r - l + 1);
    }

    /*
     * Remove every interval which is completely contained
     * inside another interval.
     */
    static ArrayList<Interval> removeContained(ArrayList<Interval> all) {
        all.sort((a, b) -> {
            if (a.l != b.l)
                return Long.compare(a.l, b.l);

            if (a.r != b.r)
                return Long.compare(b.r, a.r);

            return Integer.compare(a.col, b.col);
        });

        ArrayList<Interval> useful = new ArrayList<>();

        long maxR = Long.MIN_VALUE;

        for (Interval cur : all) {
            if (cur.r <= maxR) {
                continue;
            }

            useful.add(cur);
            maxR = cur.r;
        }

        useful.sort((a, b) -> {
            if (a.l != b.l)
                return Long.compare(a.l, b.l);

            return Long.compare(a.r, b.r);
        });

        return useful;
    }

    /*
     * Solve one chain of overlapping intervals.
     */
    static ArrayList<Long> solveChain(ArrayList<Interval> chain) {

        int k = chain.size();

        ArrayList<Long> answer = new ArrayList<>();

        if (k == 1) {
            answer.add(chain.get(0).length());
            return answer;
        }

        long[] ov = new long[k - 1];

        for (int i = 0; i + 1 < k; i++) {
            ov[i] = overlap(chain.get(i), chain.get(i + 1));
        }

        /*
         * base[i] = part of interval i which does not belong
         * to either of its overlaps.
         */
        long[] base = new long[k];

        for (int i = 0; i < k; i++) {
            long x = chain.get(i).length();

            if (i > 0)
                x -= ov[i - 1];

            if (i + 1 < k)
                x -= ov[i];

            base[i] = x;
        }

        /*
         * For interval i there are at most four possible final lengths:
         *
         * base
         * base + leftOverlap
         * base + rightOverlap
         * base + leftOverlap + rightOverlap
         *
         * Compress these lengths so every length gets a bit position.
         */
        long[] possible = new long[4 * k];
        int pc = 0;

        for (int i = 0; i < k; i++) {

            long left = (i > 0 ? ov[i - 1] : 0);
            long right = (i + 1 < k ? ov[i] : 0);

            long[] vals = {
                    base[i],
                    base[i] + left,
                    base[i] + right,
                    base[i] + left + right
            };

            for (long x : vals) {
                if (x > 0)
                    possible[pc++] = x;
            }
        }

        Arrays.sort(possible, 0, pc);

        int unique = 0;

        for (int i = 0; i < pc; i++) {
            if (unique == 0 || possible[i] != possible[unique - 1]) {
                possible[unique++] = possible[i];
            }
        }

        long[] lengths = Arrays.copyOf(possible, unique);

        /*
         * weight(rank) = 2^(rank * SHIFT)
         *
         * The SHIFT bits represent the number of segments
         * having that particular length.
         *
         * Since SHIFT = 16 and k <= 3000, no field can overflow.
         */
        BigInteger[] weight = new BigInteger[unique];

        for (int i = 0; i < unique; i++) {
            weight[i] = BigInteger.ONE.shiftLeft(i * SHIFT);
        }

        /*
         * State:
         *
         * 0 -> the previous overlap belongs to the previous interval,
         *      so current interval does NOT get its left overlap.
         *
         * 1 -> current interval gets its left overlap.
         */
        BigInteger[] dp = new BigInteger[2];
        dp[0] = BigInteger.ZERO;
        dp[1] = null;

        int[][] parent = new int[k][2];
        int[][] edgeChoice = new int[k][2];

        for (int[] row : parent)
            Arrays.fill(row, -1);

        for (int[] row : edgeChoice)
            Arrays.fill(row, -1);

        /*
         * Process all intervals except the last one.
         */
        for (int i = 0; i < k - 1; i++) {

            BigInteger[] ndp = new BigInteger[2];

            for (int state = 0; state <= 1; state++) {

                if (dp[state] == null)
                    continue;

                long left = (state == 1 ? ov[i - 1] : 0);

                if (i == 0)
                    left = 0;

                /*
                 * right = 1:
                 * current interval gets the right overlap.
                 *
                 * right = 0:
                 * next interval gets the right overlap.
                 */
                for (int right = 0; right <= 1; right++) {

                    long curLength =
                            base[i]
                            + left
                            + (right == 1 ? ov[i] : 0);

                    BigInteger candidate = dp[state];

                    if (curLength > 0) {
                        int rank = Arrays.binarySearch(
                                lengths, curLength
                        );

                        candidate = candidate.add(weight[rank]);
                    }

                    /*
                     * If current gets right overlap,
                     * next does not get left overlap.
                     *
                     * Otherwise next gets left overlap.
                     */
                    int nextState = (right == 1 ? 0 : 1);

                    if (ndp[nextState] == null ||
                            candidate.compareTo(ndp[nextState]) > 0) {

                        ndp[nextState] = candidate;
                        parent[i + 1][nextState] = state;
                        edgeChoice[i][nextState] = right;
                    }
                }
            }

            dp = ndp;
        }

        /*
         * Final interval has no right overlap.
         */
        BigInteger bestScore = null;
        int bestState = -1;

        for (int state = 0; state <= 1; state++) {

            if (dp[state] == null)
                continue;

            long left = (state == 1 ? ov[k - 2] : 0);

            long curLength = base[k - 1] + left;

            BigInteger candidate = dp[state];

            if (curLength > 0) {
                int rank = Arrays.binarySearch(lengths, curLength);
                candidate = candidate.add(weight[rank]);
            }

            if (bestScore == null ||
                    candidate.compareTo(bestScore) > 0) {

                bestScore = candidate;
                bestState = state;
            }
        }

        /*
         * Reconstruct which side gets every overlap.
         */
        int[] chosenRight = new int[k - 1];

        int state = bestState;

        for (int i = k - 2; i >= 0; i--) {

            chosenRight[i] = edgeChoice[i][state];

            state = parent[i + 1][state];
        }

        /*
         * Reconstruct final segment lengths.
         */
        int leftState = 0;

        for (int i = 0; i < k - 1; i++) {

            long left = (leftState == 1 ? ov[i - 1] : 0);

            if (i == 0)
                left = 0;

            long right =
                    (chosenRight[i] == 1 ? ov[i] : 0);

            long curLength = base[i] + left + right;

            if (curLength > 0)
                answer.add(curLength);

            /*
             * If current interval got the right overlap,
             * next interval does not get its left overlap.
             */
            leftState = (chosenRight[i] == 1 ? 0 : 1);
        }

        /*
         * Last interval.
         */
        long left = (leftState == 1 ? ov[k - 2] : 0);
        long lastLength = base[k - 1] + left;

        if (lastLength > 0)
            answer.add(lastLength);

        return answer;
    }

    public static void main(String[] args) throws Exception {

        FastScanner fs = new FastScanner();
        StringBuilder out = new StringBuilder();

        int t = fs.nextInt();

        while (t-- > 0) {

            int n = fs.nextInt();
            int m = fs.nextInt();

            ArrayList<Interval> intervals =
                    new ArrayList<>(n + m);

            for (int i = 0; i < n; i++) {
                long l = fs.nextLong();
                long r = fs.nextLong();

                intervals.add(new Interval(l, r, 0));
            }

            for (int i = 0; i < m; i++) {
                long l = fs.nextLong();
                long r = fs.nextLong();

                intervals.add(new Interval(l, r, 1));
            }

            /*
             * Intervals completely contained in another
             * interval are useless.
             */
            intervals = removeContained(intervals);

            /*
             * Split remaining intervals into chains.
             */
            ArrayList<ArrayList<Interval>> chains =
                    new ArrayList<>();

            ArrayList<Interval> current =
                    new ArrayList<>();

            for (Interval x : intervals) {

                if (current.isEmpty()) {
                    current.add(x);
                } else {

                    Interval last =
                            current.get(current.size() - 1);

                    /*
                     * Overlap exists.
                     */
                    if (x.l <= last.r) {
                        current.add(x);
                    } else {
                        chains.add(current);

                        current = new ArrayList<>();
                        current.add(x);
                    }
                }
            }

            if (!current.isEmpty())
                chains.add(current);

            ArrayList<Long> answer = new ArrayList<>();

            /*
             * Every chain is independent.
             */
            for (ArrayList<Interval> chain : chains) {
                answer.addAll(solveChain(chain));
            }

            /*
             * Required output:
             * lengths in non-increasing order.
             */
            answer.sort(Collections.reverseOrder());

            out.append(answer.size()).append('\n');

            for (long x : answer) {
                out.append(x).append(' ');
            }

            out.append('\n');
        }

        System.out.print(out);
    }
}