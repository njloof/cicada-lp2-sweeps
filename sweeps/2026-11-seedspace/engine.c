/* engine.c — campaign #28 Track C seed-space engine (PREREG f1ab025 + addendum).
 *
 * Generator cores are TRANSCRIBED from dukotah's grind27.c / grind28.c
 * (MIT license, (c) 2026 Dukotah) — CPython-2.7 MT19937 (init_by_array,
 * genrand_int32, genrand_res53, random29 reducer) and the php-src MT19937
 * engine (both twists, BADSCALING + mod reductions). Their code is
 * |delta|=0-validated against real binaries by their authors; OUR engine is
 * re-validated: V1 = 64/64 seeds vs pinned vectors.json, V2 = 8 seeds x
 * 2000 draws x 4 combos vs pinned gen28.py reference (both via drive.py).
 * The SCORER, screen, plants, null and verdicts are OURS (PREREG.md).
 *
 * Primary statistic (PREREG + addendum): skip-tolerant quadgram-LL beam
 * screen of the 120-rune corpus head, beam width 16, key advance 1..3 per
 * rune, <=12 extra consumptions, 3.0 nats/extra, initial context THE.
 * (Exact Viterbi is infeasible — letter context is path-dependent; the
 * addendum registers the width-16 beam as the primary statistic; plants
 * measure ITS power.)
 *
 * Lanes: A = Py2.7 init_by_array([w]) + random29; B = PHP init_genrand(w),
 * MT_RAND_MT19937 twist; C = PHP legacy MT_RAND_PHP twist. B/C score both
 * reductions (scale, mod) from shared draws. All lanes: signs +1 and -1.
 *
 * Build: cc -O3 -std=gnu11 -o seedspace_engine engine.c -lm
 * Modes:
 *   --ks lane seed n [scale|mod]     keystream symbols, space-separated
 *   --bench lane N quad corpus       throughput measurement
 *   --sweep lane from to quad corpus outdir    checkpointed sweep
 *   --score lane seed sign red quad file       primary score of one combo
 *   --decode lane seed sign red quad corpus    full-length beam decode -> letters
 * red: none|scale|mod   sign: 1|-1
 */
#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <math.h>

/* ---------------------------------------------------------------- CPython 2.7 MT (grind27.c, MIT (c) Dukotah) */
#define NMT 624
#define MMT 397
typedef struct { uint32_t mt[NMT]; int idx; } MT;

static void py_init_genrand(MT *r, uint32_t s) {
    r->mt[0] = s;
    for (int i = 1; i < NMT; i++)
        r->mt[i] = 1812433253u * (r->mt[i-1] ^ (r->mt[i-1] >> 30)) + (uint32_t)i;
    r->idx = NMT;
}
static void py_init_by_array(MT *r, const uint32_t *key, int klen) {
    py_init_genrand(r, 19650218u);
    int i = 1, j = 0, k = NMT > klen ? NMT : klen;
    while (k--) {
        r->mt[i] = ((r->mt[i] ^ ((r->mt[i-1] ^ (r->mt[i-1] >> 30)) * 1664525u))
                    + key[j] + (uint32_t)j);
        i++; j++;
        if (i >= NMT) { r->mt[0] = r->mt[NMT-1]; i = 1; }
        if (j >= klen) j = 0;
    }
    for (k = NMT - 1; k; k--) {
        r->mt[i] = ((r->mt[i] ^ ((r->mt[i-1] ^ (r->mt[i-1] >> 30)) * 1566083941u))
                    - (uint32_t)i);
        i++;
        if (i >= NMT) { r->mt[0] = r->mt[NMT-1]; i = 1; }
    }
    r->mt[0] = 0x80000000u;
    r->idx = NMT;
}
static inline uint32_t py_u32(MT *r) {
    if (r->idx >= NMT) {
        for (int kk = 0; kk < NMT - MMT; kk++) {
            uint32_t y = (r->mt[kk] & 0x80000000u) | (r->mt[kk+1] & 0x7FFFFFFFu);
            r->mt[kk] = r->mt[kk+MMT] ^ (y >> 1) ^ ((y & 1u) ? 0x9908B0DFu : 0u);
        }
        for (int kk = NMT - MMT; kk < NMT - 1; kk++) {
            uint32_t y = (r->mt[kk] & 0x80000000u) | (r->mt[kk+1] & 0x7FFFFFFFu);
            r->mt[kk] = r->mt[kk+(MMT-NMT)] ^ (y >> 1) ^ ((y & 1u) ? 0x9908B0DFu : 0u);
        }
        uint32_t y = (r->mt[NMT-1] & 0x80000000u) | (r->mt[0] & 0x7FFFFFFFu);
        r->mt[NMT-1] = r->mt[MMT-1] ^ (y >> 1) ^ ((y & 1u) ? 0x9908B0DFu : 0u);
        r->idx = 0;
    }
    uint32_t y = r->mt[r->idx++];
    y ^= y >> 11;
    y ^= (y << 7)  & 0x9D2C5680u;
    y ^= (y << 15) & 0xEFC60000u;
    y ^= y >> 18;
    return y;
}
static inline double py_random(MT *r) {
    uint32_t a = py_u32(r) >> 5, b = py_u32(r) >> 6;
    return (a * 67108864.0 + b) * (1.0 / 9007199254740992.0);
}
static void ks_py27(uint32_t w, uint8_t *ks, int n) {   /* random29, 2 draws/sym */
    MT r; uint32_t key[1] = { w };
    py_init_by_array(&r, key, 1);
    for (int i = 0; i < n; i++) ks[i] = (uint8_t)(int)(py_random(&r) * 29.0);
}

/* ---------------------------------------------------------------- php-src MT19937 (grind28.c, MIT (c) Dukotah) */
typedef struct { uint32_t st[624]; int cnt, php_mode; } PhpMT;
#define PHP_MIX(u, v)  (((u) & 0x80000000u) | ((v) & 0x7FFFFFFFu))
#define PHP_TWIST(m, u, v)  ((m) ^ (PHP_MIX(u, v) >> 1) ^ (((v) & 1u) ? 0x9908B0DFu : 0u))
#define PHP_TWISTP(m, u, v) ((m) ^ (PHP_MIX(u, v) >> 1) ^ (((u) & 1u) ? 0x9908B0DFu : 0u))

static void php_init(PhpMT *g, uint32_t seed, int php_mode) {
    g->st[0] = seed;
    for (int i = 1; i < 624; i++)
        g->st[i] = 1812433253u * (g->st[i-1] ^ (g->st[i-1] >> 30)) + (uint32_t)i;
    g->cnt = 624; g->php_mode = php_mode;
}
static void php_reload(PhpMT *g) {
    uint32_t *s = g->st;
    if (!g->php_mode) {
        for (int p = 0; p < 227; p++)   s[p] = PHP_TWIST(s[p+397], s[p], s[p+1]);
        for (int p = 227; p < 623; p++) s[p] = PHP_TWIST(s[p-227], s[p], s[p+1]);
        s[623] = PHP_TWIST(s[396], s[623], s[0]);
    } else {
        for (int p = 0; p < 227; p++)   s[p] = PHP_TWISTP(s[p+397], s[p], s[p+1]);
        for (int p = 227; p < 623; p++) s[p] = PHP_TWISTP(s[p-227], s[p], s[p+1]);
        s[623] = PHP_TWISTP(s[396], s[623], s[0]);
    }
    g->cnt = 0;
}
static inline uint32_t php_rand31(PhpMT *g) {
    if (g->cnt >= 624) php_reload(g);
    uint32_t y = g->st[g->cnt++];
    y ^= y >> 11;
    y ^= (y << 7)  & 0x9D2C5680u;
    y ^= (y << 15) & 0xEFC60000u;
    y ^= y >> 18;
    return y >> 1;
}
static inline uint8_t php_badscale(uint32_t r31) {
    return (uint8_t)(int)(29.0 * ((double)r31 / 2147483648.0));
}
static void ks_php(uint32_t w, int twist_php, uint8_t *ks_scale, uint8_t *ks_mod, int n) {
    PhpMT g; php_init(&g, w, twist_php);
    for (int i = 0; i < n; i++) {
        uint32_t r = php_rand31(&g);
        ks_scale[i] = php_badscale(r);
        ks_mod[i]    = (uint8_t)(r % 29u);
    }
}

/* ---------------------------------------------------------------- quadgram model */
#define NCTX 17576
static float ll[NCTX * 26];

static void load_quad(const char *path) {
    static double wch[NCTX * 26];
    static double csum[NCTX];
    double tot[26] = {0}, T = 0;
    FILE *f = fopen(path, "r");
    if (!f) { fprintf(stderr, "engine: cannot open quad file\n"); exit(3); }
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

/* rune -> letters (core/validate.TRANS) */
static const char *TRANS[29] = {
    "F","U","TH","O","R","C","G","W","H","N","I","J","EO","P","X","S","T","B",
    "E","M","L","NG","OE","D","A","AE","Y","IA","EA"
};
#define CTX_THE ((19*26+7)*26+4)   /* T,H,E */

/* ---------------------------------------------------------------- screen (primary statistic) */
#define MAXEXTRA 12
#define PEN 3.0f
#define NKS_HEAD 140

/* Primary statistic (PREREG addendum): deterministic DP over the 13
 * extra-consumption states (0..12), each state carrying its own best score
 * AND its letter context (the exact Viterbi would need ctx in the state;
 * carrying one ctx per extra-state is the registered deterministic
 * relaxation). Advances 1..3 per rune, 3.0 nats per extra consumption. */
#define NEG (-1e30f)

static float screen(const uint8_t *ks, int nks, const uint8_t *c, int L, int sign, int W) {
    (void)W;
    float ds[MAXEXTRA + 1], ds2[MAXEXTRA + 1];
    uint16_t cs[MAXEXTRA + 1], cs2[MAXEXTRA + 1];
    for (int e = 0; e <= MAXEXTRA; e++) { ds[e] = NEG; cs[e] = 0; }
    ds[0] = 0.0f; cs[0] = CTX_THE;
    for (int t = 0; t < L; t++) {
        for (int e = 0; e <= MAXEXTRA; e++) ds2[e] = NEG;
        for (int e = 0; e <= MAXEXTRA; e++) {
            if (ds[e] == NEG) continue;
            int kpos = t + e;
            if (kpos >= nks) continue;
            for (int a = 1; a <= 3; a++) {
                int e2 = e + a - 1;
                if (e2 > MAXEXTRA) continue;
                int p = (int)c[t] - sign * (int)ks[kpos];
                p %= 29; if (p < 0) p += 29;
                float s = ds[e] - PEN * (float)(a - 1);
                uint16_t ctx = cs[e];
                for (const char *q = TRANS[p]; *q; q++) {
                    s += ll[ctx * 26 + (*q - 'A')];
                    ctx = (uint16_t)((ctx % 676) * 26 + (*q - 'A'));
                }
                if (s > ds2[e2]) { ds2[e2] = s; cs2[e2] = ctx; }
            }
        }
        for (int e = 0; e <= MAXEXTRA; e++) { ds[e] = ds2[e]; cs[e] = cs2[e]; }
    }
    float best = NEG;
    for (int e = 0; e <= MAXEXTRA; e++) if (ds[e] > best) best = ds[e];
    return best;
}

/* ---------------------------------------------------------------- lanes */
enum { LANE_A, LANE_B, LANE_C };
static int lane_of(const char *s) {
    if (!strcmp(s, "A")) return LANE_A;
    if (!strcmp(s, "B")) return LANE_B;
    if (!strcmp(s, "C")) return LANE_C;
    fprintf(stderr, "engine: lane must be A|B|C\n"); exit(2);
}
static const int LANE_NRED[3] = {1, 2, 2};   /* A: random29; B/C: scale, mod */

/* top-K heap (min at root) + histogram */
typedef struct { float s; uint64_t seed; int sign, red; } Cand;
#define TOPK 1024
static Cand heap[TOPK]; static int hlen = 0;

static int cand_less(const Cand *a, const Cand *b) { return a->s < b->s; }
static void siftup(int i) {   /* min-heap fix downward */
    for (;;) {
        int l = 2*i+1, r = l+1, m = i;
        if (l < hlen && cand_less(&heap[l], &heap[m])) m = l;
        if (r < hlen && cand_less(&heap[r], &heap[m])) m = r;
        if (m == i) break;
        Cand t = heap[m]; heap[m] = heap[i]; heap[i] = t; i = m;
    }
}
static void siftdown(int i) {
    while (i > 0) {
        int p = (i - 1) / 2;
        if (!cand_less(&heap[i], &heap[p])) break;
        Cand t = heap[p]; heap[p] = heap[i]; heap[i] = t; i = p;
    }
}
static void heap_push(float s, uint64_t seed, int sign, int red) {
    if (hlen < TOPK) {
        heap[hlen++] = (Cand){s, seed, sign, red}; siftdown(hlen - 1);
    } else if (s > heap[0].s) {
        heap[0] = (Cand){s, seed, sign, red}; siftup(0);
    }
}
static void heap_build(void) { for (int i = hlen/2 - 1; i >= 0; i--) siftup(i); }
static int cand_cmp(const void *A, const void *B) {  /* score desc for output */
    const Cand *a = A, *b = B;
    if (a->s != b->s) return a->s < b->s ? 1 : -1;
    return a->seed < b->seed ? -1 : (a->seed > b->seed);
}

/* histogram: 0.5-nat bins over [-500, 200) */
#define HBINS 1400
static uint64_t hist[HBINS];
static inline void hbump(float s) {
    int b = (int)((s + 500.0f) * 2.0f);
    if (b < 0) b = 0; if (b >= HBINS) b = HBINS - 1;
    hist[b]++;
}

static void note_all(float s, int sign, int red, uint64_t seed) {
    hbump(s); heap_push(s, seed, sign, red);
}

/* score one seed, all combos of a lane; note(s,sign,red,seed) per combo; best returned */
static float score_seed(int lane, uint32_t w, const uint8_t *c, int L, int W,
                        void (*note)(float, int, int, uint64_t), uint64_t seed) {
    static uint8_t ks[NKS_HEAD], ks2[NKS_HEAD];
    float best = -1e30f;
    int nred = LANE_NRED[lane];
    if (lane == LANE_A) ks_py27(w, ks, NKS_HEAD);
    else ks_php(w, lane == LANE_C, ks, ks2, NKS_HEAD);
    for (int red = 0; red < nred; red++) {
        const uint8_t *k = (lane == LANE_A || red == 0) ? ks : ks2;
        for (int si = 0; si < 2; si++) {
            int sign = si ? 1 : -1;
            float s = screen(k, NKS_HEAD, c, L, sign, W);
            if (note) note(s, sign, red, seed);
            if (s > best) best = s;
        }
    }
    return best;
}

/* ---------------------------------------------------------------- corpus */
#define LMAX 13000
static uint8_t corpus[LMAX];
static int read_corpus(const char *p) {
    FILE *f = fopen(p, "rb");
    if (!f) { fprintf(stderr, "engine: corpus open fail\n"); exit(2); }
    int n = (int)fread(corpus, 1, LMAX, f);
    fclose(f);
    for (int i = 0; i < n; i++)
        if (corpus[i] > 28) { fprintf(stderr, "engine: corpus byte %d > 28\n", corpus[i]); exit(2); }
    if (n == 0) { fprintf(stderr, "engine: corpus empty\n"); exit(2); }
    return n;
}

/* ---------------------------------------------------------------- checkpoint state
 * ONE file per lane, committed atomically (tmp + rename): cursor, histogram,
 * top-K. A crash loses at most one chunk and resume re-runs exactly the seeds
 * whose results were never persisted — no histogram double-counting. */
static void save_state(const char *outdir, char ln, uint64_t cursor) {
    char path[512], tmp[560]; FILE *f;
    snprintf(path, sizeof path, "%s/state_%c.txt", outdir, ln);
    snprintf(tmp, sizeof tmp, "%s/state_%c.txt.tmp", outdir, ln);
    f = fopen(tmp, "w");
    fprintf(f, "CURSOR %llu\nHIST\n", (unsigned long long)cursor);
    for (int b = 0; b < HBINS; b++)
        if (hist[b]) fprintf(f, "%d %llu\n", b, (unsigned long long)hist[b]);
    fprintf(f, "TOP\n");
    for (int i = 0; i < hlen; i++)
        fprintf(f, "%.4f %llu %d %d\n", heap[i].s, (unsigned long long)heap[i].seed,
                heap[i].sign, heap[i].red);
    if (fflush(f) || fsync(fileno(f)) || fclose(f)) { fprintf(stderr, "engine: state write fail\n"); exit(4); }
    if (rename(tmp, path)) { fprintf(stderr, "engine: state rename fail\n"); exit(4); }
}
static void load_state(const char *outdir, char ln, uint64_t *cursor) {
    char path[512]; FILE *f;
    snprintf(path, sizeof path, "%s/state_%c.txt", outdir, ln);
    if (!(f = fopen(path, "r"))) return;
    char line[256]; int section = 0;
    while (fgets(line, sizeof line, f)) {
        if (!strncmp(line, "CURSOR ", 7)) { sscanf(line + 7, "%llu", (unsigned long long*)cursor); continue; }
        if (!strncmp(line, "HIST", 4)) { section = 1; continue; }
        if (!strncmp(line, "TOP", 3))   { section = 2; continue; }
        if (section == 1) {
            int b; unsigned long long n;
            if (sscanf(line, "%d %llu", &b, &n) == 2 && b >= 0 && b < HBINS) hist[b] += n;
        } else if (section == 2 && hlen < TOPK) {
            float s; unsigned long long sd; int sg, rd;
            if (sscanf(line, "%f %llu %d %d", &s, &sd, &sg, &rd) == 4)
                heap[hlen++] = (Cand){s, sd, sg, rd};
        }
    }
    fclose(f);
    heap_build();
}
static void write_final(const char *outdir, char ln) {
    char path[512]; FILE *f;
    qsort(heap, (size_t)hlen, sizeof(Cand), cand_cmp);
    snprintf(path, sizeof path, "%s/top_%c.tsv", outdir, ln);
    f = fopen(path, "w");
    for (int i = 0; i < hlen; i++)
        fprintf(f, "%.4f\t%llu\t%d\t%d\n", heap[i].s, (unsigned long long)heap[i].seed,
                heap[i].sign, heap[i].red);
    fclose(f);
    snprintf(path, sizeof path, "%s/hist_%c.txt", outdir, ln);
    f = fopen(path, "w");
    for (int b = 0; b < HBINS; b++) fprintf(f, "%.1f\t%llu\n", -500.0f + b * 0.5f,
                                            (unsigned long long)hist[b]);
    fclose(f);
}

/* ---------------------------------------------------------------- modes */
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "engine: need a mode\n"); return 2; }
    const char *mode = argv[1];

    if (!strcmp(mode, "--ks")) {   /* --ks lane seed n [scale|mod] */
        int lane = lane_of(argv[2]); uint32_t w = (uint32_t)strtoul(argv[3], 0, 10);
        int n = atoi(argv[4]);
        static uint8_t ks[30000], ks2[30000];
        if (lane == LANE_A) {
            if (n > 30000) return 2;
            ks_py27(w, ks, n);
            for (int i = 0; i < n; i++) printf("%d%s", ks[i], i == n-1 ? "\n" : " ");
        } else {
            if (n > 30000) return 2;
            ks_php(w, lane == LANE_C, ks, ks2, n);
            const char *red = argc > 5 ? argv[5] : "scale";
            const uint8_t *k = strcmp(red, "mod") ? ks : ks2;
            for (int i = 0; i < n; i++) printf("%d%s", k[i], i == n-1 ? "\n" : " ");
        }
        return 0;
    }
    if (!strcmp(mode, "--bench")) {  /* --bench lane N quad corpus */
        int lane = lane_of(argv[2]); uint64_t N = strtoull(argv[3], 0, 10);
        load_quad(argv[4]); int L = read_corpus(argv[5]); if (L > 120) L = 120;
        struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
        float best = -1e30f; uint64_t hit = 0;
        for (uint64_t w = 0; w < N; w++) {
            float s = score_seed(lane, (uint32_t)w, corpus, L, 16, NULL, 0);
            if (s > best) { best = s; hit = w; }
        }
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double dt = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
        printf("lane=%c seeds=%llu secs=%.2f seeds_per_s=%.0f best=%.3f@%llu\n",
               "ABC"[lane], (unsigned long long)N, dt, N / dt, best, (unsigned long long)hit);
        return 0;
    }
    if (!strcmp(mode, "--score")) {  /* --score lane seed sign red quad file */
        int lane = lane_of(argv[2]); uint32_t w = (uint32_t)strtoul(argv[3], 0, 10);
        int sign = atoi(argv[4]); const char *red = argv[5];
        load_quad(argv[6]); int L = read_corpus(argv[7]); if (L > 120) L = 120;
        static uint8_t ks[NKS_HEAD], ks2[NKS_HEAD];
        if (lane == LANE_A) ks_py27(w, ks, NKS_HEAD);
        else ks_php(w, lane == LANE_C, ks, ks2, NKS_HEAD);
        const uint8_t *k = (lane == LANE_A || !strcmp(red, "scale")) ? ks : ks2;
        printf("%.4f\n", screen(k, NKS_HEAD, corpus, L, sign, 16));
        return 0;
    }
    if (!strcmp(mode, "--decode")) { /* --decode lane seed sign red quad corpus */
        int lane = lane_of(argv[2]); uint32_t w = (uint32_t)strtoul(argv[3], 0, 10);
        int sign = atoi(argv[4]); const char *red = argv[5];
        load_quad(argv[6]); int L = read_corpus(argv[7]);
        int nks = L + 1200 + 8;
        uint8_t *ks = malloc((size_t)nks), *ks2 = malloc((size_t)nks);
        if (lane == LANE_A) ks_py27(w, ks, nks);
        else ks_php(w, lane == LANE_C, ks, ks2, nks);
        const uint8_t *k = (lane == LANE_A || !strcmp(red, "scale")) ? ks : ks2;
        /* full-length beam: width 64, extra cap 1200, backpointers per sorted slot */
        #define W64 64
        #define NCAND (W64 * 3)
        #define MAXEX2 1200
        typedef struct { float s; int extra; uint16_t ctx; } St2;
        static St2 cur[W64], nxt[NCAND];
        static uint8_t bprev[LMAX][NCAND], brune[LMAX][NCAND];
        int nc = 1;
        cur[0].s = 0; cur[0].extra = 0; cur[0].ctx = CTX_THE;
        for (int t = 0; t < L; t++) {
            int nn = 0;
            for (int i = 0; i < nc && nn + 3 <= NCAND; i++)
                for (int a = 1; a <= 3; a++) {
                    int e = cur[i].extra + a - 1;
                    if (e > MAXEX2) continue;
                    int kpos = t + cur[i].extra;
                    if (kpos >= nks) continue;
                    int p = (int)corpus[t] - sign * (int)k[kpos];
                    p %= 29; if (p < 0) p += 29;
                    float s = cur[i].s - PEN * (float)(a - 1);
                    uint16_t ctx = cur[i].ctx;
                    for (const char *q = TRANS[p]; *q; q++) {
                        s += ll[ctx * 26 + (*q - 'A')];
                        ctx = (uint16_t)((ctx % 676) * 26 + (*q - 'A'));
                    }
                    nxt[nn] = (St2){s, e, ctx};
                    bprev[t][nn] = (uint8_t)i; brune[t][nn] = (uint8_t)p;
                    nn++;
                }
            /* insertion sort desc (nn <= 192), carrying backpointers */
            for (int i = 1; i < nn; i++) {
                St2 s2 = nxt[i]; uint8_t p1 = bprev[t][i], p3 = brune[t][i];
                int j = i - 1;
                while (j >= 0 && nxt[j].s < s2.s) {
                    nxt[j+1] = nxt[j]; bprev[t][j+1] = bprev[t][j]; brune[t][j+1] = brune[t][j];
                    j--;
                }
                nxt[j+1] = s2; bprev[t][j+1] = p1; brune[t][j+1] = p3;
            }
            nc = nn < W64 ? nn : W64;
            for (int i = 0; i < nc; i++) cur[i] = nxt[i];
        }
        /* backtrack from best final state (slot 0 = best) */
        char *out = malloc((size_t)(2 * L + 8)); int ol = 0;
        int state = 0;
        for (int t = L - 1; t >= 0; t--) {
            int p = brune[t][state];
            const char *lt = TRANS[p]; int l2 = (int)strlen(lt);
            for (int m = l2 - 1; m >= 0; m--) out[ol++] = lt[m];
            state = bprev[t][state];
        }
        for (int i = ol - 1; i >= 0; i--) putchar(out[i]);
        putchar('\n');
        return 0;
    }
    if (!strcmp(mode, "--sweep")) { /* --sweep lane from to quad corpus outdir */
        int lane = lane_of(argv[2]);
        uint64_t from = strtoull(argv[3], 0, 10), to = strtoull(argv[4], 0, 10);
        load_quad(argv[5]); int L = read_corpus(argv[6]); if (L > 120) L = 120;
        const char *outdir = argv[7];
        char ln = "ABC"[lane];
        uint64_t cursor = from;
        load_state(outdir, ln, &cursor);
        if (cursor < from) cursor = from;
        struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
        uint64_t done0 = cursor;
        for (; cursor < to; cursor++) {
            score_seed(lane, (uint32_t)cursor, corpus, L, 16, note_all, cursor);
            if ((cursor - done0) % 2000000 == 1999999) {
                save_state(outdir, ln, cursor + 1);
                clock_gettime(CLOCK_MONOTONIC, &t1);
                double dt = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
                fprintf(stderr, "lane %c cursor %llu rate %.0f/s\n", ln,
                        (unsigned long long)(cursor + 1), dt > 0 ? (cursor + 1 - done0) / dt : 0.0);
                t0 = t1; done0 = cursor + 1;
            }
        }
        save_state(outdir, ln, cursor);
        write_final(outdir, ln);
        return 0;
    }
    fprintf(stderr, "engine: unknown mode\n");
    return 2;
}
