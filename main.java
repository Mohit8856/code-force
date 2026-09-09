import java.util.*;

public class main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        int t = sc.nextInt();

        while (t-- > 0) {

            int n = sc.nextInt();

            int[] a = new int[n];
            int zeroCount = 0;

            for (int i = 0; i < n; i++) {
                a[i] = sc.nextInt();

                if (a[i] == 0) {
                    zeroCount++;
                }
            }

            // Exactly one zero is impossible
            if (zeroCount == 1) {
                System.out.println("NO");
                continue;
            }

            System.out.println("YES");

            StringBuilder ans = new StringBuilder();

            boolean firstZero = true;

            for (int i = 0; i < n; i++) {

                if (a[i] != 0) {
                    // All non-zero elements go to A
                    ans.append('A');
                }
                else if (firstZero) {
                    // First zero goes to C
                    ans.append('C');
                    firstZero = false;
                }
                else {
                    // Second and remaining zeros go to B
                    ans.append('B');
                }
            }

            System.out.println(ans);
        }

        sc.close();
    }
}