import java.math.BigInteger;
import java.util.Scanner;

public class A {

    private static final BigInteger c = new BigInteger("17777777777777777777777777777777777777777777777777777777777777777777777777737777776057", 8);

    public static class aa {
        public BigInteger aaa, bbb;

        public aa() {
        }

        public aa(BigInteger aaa, BigInteger bbb) {
            this.aaa = aaa;
            this.bbb = bbb;
        }

        @Override
        public String toString() {
            return "(" + aaa.toString(16) + ", " + bbb.toString(16) + ")";
        }

        public boolean equals(aa a) {
            return this.aaa.equals(a.aaa) && this.bbb.equals(a.bbb);
        }
    }

    private static BigInteger w(BigInteger a, BigInteger b) {
        return a.add(b).mod(c);
    }

    private static BigInteger x(BigInteger a, BigInteger b) {
        return a.subtract(b).mod(c);
    }

    private static BigInteger y(BigInteger a, BigInteger b) {
        return a.multiply(b).mod(c);
    }

    private static BigInteger z(BigInteger a, BigInteger b) {
        return y(a, b.modInverse(c));
    }

    public static aa zzz(aa a, aa b) {

        if (a.aaa.equals(b.aaa)) {
            BigInteger o = y(BigInteger.valueOf(3), a.aaa.pow(2));
            BigInteger p = y(BigInteger.valueOf(2), a.bbb);
            BigInteger q = z(o, p);
            BigInteger r = x(q.pow(2), y(BigInteger.valueOf(2), a.aaa));
            BigInteger s = x(y(q, x(a.aaa, r)), a.bbb);
            return new aa(r, s);
        } else {
            BigInteger c = z(x(b.bbb, a.bbb), x(b.aaa, a.aaa));
            BigInteger r = x(x(c.pow(2), a.aaa), b.aaa);
            BigInteger s = x(y(c, x(a.aaa, r)), a.bbb);
            return new aa(r, s);
        }
    }

    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);
        try {
            System.out.print("aaa: ");
            String aaa = scanner.nextLine().trim();

            System.out.print("bbb: ");
            String bbb = scanner.nextLine().trim();

            BigInteger yyy = new BigInteger(aaa, 10);
            BigInteger zzz = new BigInteger(bbb, 10);

            aa lol = new aa(yyy, zzz);
            aa lmao = new aa(new BigInteger("11615376121650374234147712415727620557267422416714444335426002334554047606566607775613", 8), new BigInteger("6077114355247325330417052411472260416432326704514764170005202327562661631377512470667", 8));
            aa rofl = new aa(new BigInteger("12077346633003322030116204134501641554466352254175203365302635013403541442703604104474", 8), new BigInteger("1530707357151505401450567744077503403305626016434143551022176207522750713220223304556", 8));
            aa kek = zzz(lol, lmao);
            if(kek.equals(rofl)) {
                System.out.println("CBC{" + lol.aaa + lol.bbb + "}");
            }
        } catch (Exception e) {
        }
        scanner.close();
    }
}

