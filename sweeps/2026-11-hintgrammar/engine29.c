/* engine29.c — Campaign #29 K1 plaintext-autokey cell (PREREG + addenda 1-3).
 *
 * K1: key stream = seed ++ P (plaintext autokey, lag w = seed length).
 * Skip-tolerance = #28 engine screen semantics (advance 1..3 per rune, 3.0
 * nats/extra, ctx-carrying deterministic relaxation) EXTENDED with per-state
 * plaintext history (the autokey key is path-dependent; addendum 3).
 * Causality cap: extra <= min(12, w-1) — with e >= w the key would index the
 * current/future plaintext (undecodable). Seed region (t < w) decoded with
 * key = seed, assumed reject-free (disclosed); window = runes [w, w+120).
 *
 *   --k1 corpus.bin quad hints.bin l1,l2,... wmin wmax
 *        -> grid over (hint, w in [wmin,wmax], off, sign); top-64 stdout:
 *           "score hintidx off w sign"
 *   --k1decode corpus.bin quad seed.bin w sign
 *        -> full-length DP, best-state plaintext history transliterated, stdout
 *
 * Scorer/nulls/verdicts are OURS; quadgram loader mirrors #28 engine.c.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define NCTX 17576
#define LMAX 13000
#define HEAD 120
#define MAXE 12
#define PEN 3.0f
#define NEG (-1e30f)

static float ll[NCTX * 26];
static const char *TRANS[29] = {
    "F","U","TH","O","R","C","G","W","H","N","I","J","EO","P","X","S","T","B",
    "E","M","L","NG","OE","D","A","AE","Y","IA","EA"
};
#define CTX_THE ((19*26+7)*26+4)

static void load_quad(const char *path) {
    static double wch[NCTX * 26];
    static double csum[NCTX];
    double tot[26] = {0}, T = 0;
    FILE *f = fopen(path, "r");
    if (!f) { fprintf(stderr, "engine29: cannot open quad file\n"); exit(3); }
    char q[8]; long long c;
    while (fscanf(f, "%4s %lld", q, &c) == 2) {
        int a = q[0]-'A', b = q[1]-'A', d = q[2]-'A', e = q[3]-'A';
        if ((unsigned)a > 25 || (unsigned)b > 25 || (unsigned)d > 25 || (unsigned)e > 25)
            continue;
        int ctx = (a * 26 + b) * 26 + d;
        wch[ctx * 26 + e] += (double)c;
        csum[ctx] += (double)c;
        tot[e] += (double)c; T += (double)c;
    }
    fclose(f);
    float uni_ll[26];
    for (int i = 0; i < 26; i++) uni_ll[i] = (float)log(tot[i] > 0 ? tot[i] / T : 1e-12);
    for (int ctx = 0; ctx < NCTX; ctx++)
        for (int e = 0; e < 26; e++)
            ll[ctx * 26 + e] = (csum[ctx] > 0 && wch[ctx * 26 + e] > 0)
                ? (float)log(wch[ctx * 26 + e] / csum[ctx])
                : uni_ll[e];
}

static uint8_t corpus[LMAX]; static int L;
static int read_corpus(const char *p) {
    FILE *f = fopen(p, "rb"); if (!f) { fprintf(stderr, "engine29: corpus\n"); exit(2); }
    L = (int)fread(corpus, 1, LMAX, f); fclose(f); return L;
}

/* one candidate DP. hist buffers [MAXE+1][LMAX]. Returns best score; if
 * full!=0 runs to L and writes best plaintext to out (len L-w). */
static float k1_dp(const uint8_t *seed, int w, const uint8_t *c, int clen,
                   int sign, int full, uint8_t *out) {
    int cap = w - 1 < MAXE ? w - 1 : MAXE;
    int tend = full ? clen : (w + HEAD < clen ? w + HEAD : clen);
    static uint8_t hA[MAXE + 1][LMAX], hB[MAXE + 1][LMAX];
    float ds[MAXE + 1], ds2[MAXE + 1];
    uint16_t cs[MAXE + 1], cs2[MAXE + 1];
    for (int e = 0; e <= cap; e++) { ds[e] = NEG; cs[e] = 0; }
    /* seed region: key = seed[r], no branching */
    for (int r = 0; r < w && r < clen; r++) {
        int p = ((int)c[r] - sign * (int)seed[r]) % 29; if (p < 0) p += 29;
        for (int e = 0; e <= cap; e++) hA[e][r] = (uint8_t)p;
    }
    ds[0] = 0.0f; cs[0] = CTX_THE;   /* window scoring starts at t=w, ctx THE */
    for (int t = w; t < tend; t++) {
        for (int e = 0; e <= cap; e++) ds2[e] = NEG;
        int any = 0;
        for (int e = 0; e <= cap; e++) {
            float s0 = ds[e]; if (s0 == NEG) continue;
            int kv = hA[e][t + e - w];            /* causality: e < w */
            int p = ((int)c[t] - sign * kv) % 29; if (p < 0) p += 29;
            float s = s0; uint16_t ctx = cs[e];
            for (const char *q = TRANS[p]; *q; q++) {
                s += ll[ctx * 26 + (*q - 'A')];
                ctx = (uint16_t)((ctx % 676) * 26 + (*q - 'A'));
            }
            for (int a = 1; a <= 3; a++) {
                int e2 = e + a - 1; if (e2 > cap) continue;
                float s2 = s - PEN * (float)(a - 1);
                if (s2 > ds2[e2]) {
                    ds2[e2] = s2; cs2[e2] = ctx;
                    memcpy(hB[e2], hA[e], (size_t)t);
                    hB[e2][t] = (uint8_t)p;
                }
            }
            any = 1;
        }
        if (!any) return NEG;
        for (int e = 0; e <= cap; e++) { ds[e] = ds2[e]; cs[e] = cs2[e]; }
        for (int e = 0; e <= cap; e++) memcpy(hA[e], hB[e], (size_t)(t + 1));
    }
    int best = 0;
    for (int e = 1; e <= cap; e++) if (ds[e] > ds[best]) best = e;
    if (full && out) memcpy(out, hA[best] + w, (size_t)(clen - w));
    return ds[best];
}

/* top-64 min-heap (array, linear insert; 64 slots) */
typedef struct { float s; int h, off, w, sign; } Cand;
#define TOPK 64
static Cand top[TOPK]; static int ntop = 0;
static float bw[65]; static int bwm[65][4];   /* per-w best (w<=64) */
static void offer(float s, int h, int off, int w, int sign) {
    if (ntop < TOPK) { top[ntop++] = (Cand){s,h,off,w,sign};
        return; }
    /* find min slot */
    int mi = 0; for (int i = 1; i < TOPK; i++) if (top[i].s < top[mi].s) mi = i;
    if (s > top[mi].s) top[mi] = (Cand){s,h,off,w,sign};
    if (w >= 2 && w <= 64 && s > bw[w]) { bw[w] = s; bwm[w][0]=h; bwm[w][1]=off; bwm[w][2]=w; bwm[w][3]=sign; }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: engine29 --k1 ... | --k1decode ...\n"); return 2; }
    if (!strcmp(argv[1], "--k1")) {
        /* --k1 corpus quad hints.bin l1,l2,... wmin wmax */
        if (argc != 8) { fprintf(stderr, "args\n"); return 2; }
        read_corpus(argv[2]); load_quad(argv[3]);
        FILE *f = fopen(argv[4], "rb"); if (!f) { fprintf(stderr, "hints\n"); return 2; }
        static uint8_t hints[65536]; int hl = (int)fread(hints, 1, 65536, f); fclose(f);
        int lens[16], nh = 0, base[16], acc = 0;
        char *ls = strdup(argv[5]), *tk = strtok(ls, ",");
        while (tk && nh < 16) { lens[nh] = atoi(tk); base[nh] = acc; acc += lens[nh]; nh++; tk = strtok(0, ","); }
        if (acc != hl) { fprintf(stderr, "engine29: hint lens %d != bytes %d\n", acc, hl); return 2; }
        int wmin = atoi(argv[6]), wmax = atoi(argv[7]);
        for (int w = 0; w < 65; w++) bw[w] = NEG;
    for (int h = 0; h < nh; h++)
            for (int w = wmin; w <= wmax; w++) {
                if (w > lens[h]) continue;
                for (int off = 0; off + w <= lens[h]; off++)
                    for (int si = 0; si < 2; si++) {
                        int sign = si ? -1 : 1;
                        float s = k1_dp(hints + base[h] + off, w, corpus, L, sign, 0, NULL);
                        offer(s, h, off, w, sign);
                    }
            }
        for (int i = 0; i < ntop; i++)
            if (top[i].s > NEG/2) printf("%.4f %d %d %d %d\n", top[i].s, top[i].h, top[i].off, top[i].w, top[i].sign);
        for (int w = wmin; w <= wmax; w++)
            if (bw[w] > NEG/2) printf("B %d %.4f %d %d %d %d\n", w, bw[w], bwm[w][0], bwm[w][1], bwm[w][2], bwm[w][3]);
        return 0;
    }
    if (!strcmp(argv[1], "--k1decode")) {
        /* --k1decode corpus quad seed.bin w sign */
        if (argc != 7) { fprintf(stderr, "args\n"); return 2; }
        read_corpus(argv[2]); load_quad(argv[3]);
        FILE *f = fopen(argv[4], "rb"); if (!f) { fprintf(stderr, "seed\n"); return 2; }
        uint8_t seed[64]; int w = atoi(argv[5]);
        if ((int)fread(seed, 1, w, f) != w) { fprintf(stderr, "seed short\n"); return 2; }
        fclose(f);
        int sign = atoi(argv[6]);
        static uint8_t out[LMAX];
        float s = k1_dp(seed, w, corpus, L, sign, 1, out);
        fprintf(stderr, "score %.4f\n", s);
        for (int i = 0; i < L - w; i++) fputs(TRANS[out[i]], stdout);
        putchar('\n');
        if (argc >= 8) { FILE *g = fopen(argv[7], "wb"); fwrite(out, 1, (size_t)(L - w), g); fclose(g); }
        return 0;
    }
    fprintf(stderr, "engine29: unknown mode\n"); return 2;
}
