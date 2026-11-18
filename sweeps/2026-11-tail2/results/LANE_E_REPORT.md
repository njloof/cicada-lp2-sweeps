# Campaign #25 Lane E (LP1 plaintext confirmation) report

Targets (9 LP1 pages >=60 runes, scream314 lineage): Runes - 01.j:184, 03.jpg:395, 04.jpg:122, 05.jpg:157, 06.jpg:742, 10.jpg - ind:629, 13.jpg - ind:125, 14.jpg - 107:320, 16.jpg - 229:89

Controls (English bar -5.2, calibrated from PT controls):
  control ANEND56 PT identity: -4.872
  control PARABLE57 PT identity: -4.421
  control p56-CT identity (must be LOW): -7.738

Plant ANEND56-PT Caesar s=13 through family: -4.872 at a=1 s=16 fwd (PASS, cell recovered)

  Runes - 01.jpg: tested best -4.478 (a=28 s=28 fwd), full-affine -4.478, identity -7.477

  03.jpg: tested best -7.029 (a=28 s=14 fwd), full-affine -6.865, identity -7.510

  04.jpg: tested best -6.977 (a=1 s=17 rev), full-affine -6.744, identity -7.722

  05.jpg: tested best -4.979 (a=1 s=0 fwd), full-affine -4.979, identity -4.979

  06.jpg: tested best -4.127 (a=28 s=2 fwd), full-affine -4.127, identity -7.168

  10.jpg - index: tested best -4.600 (a=1 s=0 fwd), full-affine -4.600, identity -4.600

  13.jpg - index: tested best -4.502 (a=1 s=0 fwd), full-affine -4.502, identity -4.502

  14.jpg - 107.j: tested best -7.037 (a=28 s=17 rev), full-affine -6.881, identity -7.527

  16.jpg - 229.j: tested best -4.720 (a=1 s=0 fwd), full-affine -4.720, identity -4.720

Per-page p (obs vs family-matched shuffle null, D=200) / Holm / null-max margin (p=0.0050 is the floor 1/201, 0/200 beats; margin shown per #24 p-floor lesson):

  Runes - 01.jpg: obs -4.478 p=0.0050 holm=0.0448 nullmax -5.865 ENGLISH-LEVEL

  05.jpg: obs -4.979 p=0.0050 holm=0.0448 nullmax -5.962 ENGLISH-LEVEL

  06.jpg: obs -4.127 p=0.0050 holm=0.0448 nullmax -6.227 ENGLISH-LEVEL

  10.jpg - index: obs -4.600 p=0.0050 holm=0.0448 nullmax -6.219 ENGLISH-LEVEL

  13.jpg - index: obs -4.502 p=0.0050 holm=0.0448 nullmax -5.842 ENGLISH-LEVEL

  16.jpg - 229.j: obs -4.720 p=0.0050 holm=0.0448 nullmax -5.538 ENGLISH-LEVEL

  03.jpg: obs -7.029 p=1.0000 holm=1.0000 nullmax -6.706 

  04.jpg: obs -6.977 p=1.0000 holm=1.0000 nullmax -6.259 

  14.jpg - 107.j: obs -7.037 p=1.0000 holm=1.0000 nullmax -6.680 

Best tested-family decodes (first 160 letters, merged):

  Runes - 01.jpg [28|28|fwd]: AWARNNGBELIEUENOTHNGFROMTHISBOOCEXCEPTWHATYOUCNOWTOBETRUETESTTHECNOWLEDGEFINDYOURTRUTHEXPERIENCEYOURDEATHDONOTEDITORCHANGETHISBOOCORTHEMESSAGECONTAINEDWITHINEIT

  05.jpg [1|0|fwd]: SOMEWISDOMTHEPRIMESARESACREDTHETOTIENTFUNCTIANISSACREDALLTHNGSSHOULDBEENCRYPTEDCNOWTHISSHADOWSAETHEREALBUFFERSUOIDCARNALOBSCURAFORMMOBIUSANALOGUOIDMOURNFULAETHE

  06.jpg [28|2|fwd]: ACOANAMANDECIDEDTOGOANDSTUDYWITHAMASTERHEWENTTOTHEDOOROFTHEMASTERWHOAREYOUWHOWISHESTOSTUDYHEREASCEDTHEMASTERTHESTUDENTTOLDTHEMASTERHISNAMETHATISNOTWHATYOUARETHA

  10.jpg - index [1|0|fwd]: THELOSSOFDIUINITYTHECIRCUMFERENCEPRACTICESTHREEBEHAUIARSWHICHCAUSETHELOSSOFDIUINITYCONSUMPTIANWECONSUMETOOMUCHBECAUSEWEBELEIUETHEFOLLWNGTWOERRORSWITHINTHEDECEPT

  13.jpg - index [1|0|fwd]: SOMEWISDOMAMASSGREATWEALTHNEUERBECOMEATTACHEDTOWHATYOUOWNBEPREPAREDTODESTROYALLTHATYOUOWNANINSTRUCTIANPROGRAMYOURMINDPROGRAMREALITY

  16.jpg - 229.j [1|0|fwd]: ANINSTRUCTIANCWESTIANALLTHNGSDISCOUERTRUTHINSIDEYOURSELFFOLLOWYOURTRUTHIMPOSENOTHNGONOTHERSCNOWTHIS

  03.jpg [28|14|fwd]: XPSOEEATHXNITHPHUSSXWFIANDSBASTHIANCEOEATTAAWEULOETIJSTARXXAEPOETHPEBUIERUENEECWYFALITRXUNTHTHENIEOUXOAJTHNWTYEWYSDEAIBOEIANEOTHEIANUWAHTHNOEUPTHNIAEWTURYBYFXDR

  04.jpg [1|17|rev]: BCOEPGCNGTHEOBUNGGOEHBXMPAEPOMTHIAFPHGOESEXOEMHEOTMHTHUEAFBEPTHXBJAUCPEATTDOERWENTIADXGTHYBNTYECUDUCWEONGEAENGTOEOEEOBUBESPOEEAXJWXGEAITEANOETHNGEANGAUBMNGWCB

  14.jpg - 107.j [28|17|rev]: OEEAREULJIAHRIEADIAIIALHIDWEOIAISRWOEOESPWXFCATAMHOEEOEXWAERITOHTIIDEOEOEEOIAIAGJNGSATHWAETMYMEOEEOOEHELHIDWEOIAISRIARFRUPPMEOIARIANXPALTHRIAMYOEHEAJPUMIAOELTHI

VERDICT: LP1-PAGE-PLAINTEXT — FLAG FOR OWNER: Runes - 01.jpg, 05.jpg, 06.jpg, 10.jpg - index.1.jpg, 13.jpg - index.4.jpg, 16.jpg - 229.jpg score English-level under a Caesar/atbash layer (new ground truth in the scream314 lineage; never auto-certified)

DISCLOSURES: (1) tested family = a in {1,28} x s x fwd/rev (corrected pre-output from full affine, priced null cost); full affine reported untested. (2) rune-shuffle null preserves rune multiset; digraph letter adjacency is broken by the shuffle (conservative). (3) scream314 lineage only (9.2% agreement with dukotah stream). (4) quadgram floor log10(0.01/N). (5) runtime 0 s [corrections-rerun with cached null, PREREG correction 2; original full run 78 s on studio].
