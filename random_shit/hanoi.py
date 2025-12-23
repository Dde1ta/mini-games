"""class Solution {
public:
    int peopleAwareOfSecret(int n, int delay, int forget) {
        vector<long long> window(n, 0);

        window[0] = 1;

        long long i = 1, ans,j = -1*(delay - 1), k = -1*(forget - 1), know = 1, share = 0, MOD = 10e9+7;

        while(i < n){
            if(j >= 0){
                share = (window[j] + MOD) % MOD;
            }
            if(k >= 0){
                share = (share - window[k] + MOD) % MOD;
            }


            window[i] = (window[i - 1] + share + MOD) % MOD;
            i ++;
            j ++;
            k ++;
        }

        if(k > 0) ans = (window[n - 1] - window[k - 1] + MOD) % MOD;
        else ans = (window[n - 1] + MOD) % MOD;
        return ans;
    }
};"""

import matplotlib.pyplot as plt

n = 600
delay = 18
forget = 200

window = [0 for i in range(n)]
x = [i for i in range(n)]
share_states = [0 for i in range(n)]

print(window, x, share_states, sep="\n")

window[0] = 1

i = 1
j = -1 * (delay - 1)
k = -1 * (forget - 1)
share = 0

MOD = 10e9 + 7

while(i < n):
    if(j >= 0):
        share = (window[j] + MOD) % MOD

    if(k >= 0):
        share = (share - window[k] + MOD) % MOD

    share_states[i] = share

    window[i] = (window[i - 1] + share + MOD) % MOD
    i += 1
    j += 1
    k += 1


plt.plot(x[550::], window[550::])
plt.plot(x[550::], share_states[550::])
plt.show()
