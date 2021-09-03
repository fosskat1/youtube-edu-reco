"""In RSA, an encryption key of e = 3 can be used so long as (p-1)(q-1) is not
divisible by 3. For p = 11 and q = 23, let e = 3. Find d. Show how one enciphers the
plaintext m = 2 with e = 3 into a value for c. Then show that deciphering c with d yields m again."""

e = 3
p=11
q=23
n=p*q # 253
print(n)


def find_d(p,q,e):
    k = 1
    totient = (p-1)*(q-1)
    while True:

        d = (1 + (k * totient))/e
        if d % 1 == 0:
            print("k: ", k)
            return d
        k += 1


# print(find_d(181,1451,154993))
print(find_d(11,23,3))
