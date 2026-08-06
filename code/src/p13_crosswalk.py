"""p13_crosswalk — slug -> US-listed company map. Curated; every match is human-verifiable via
the validation sheet. status: LISTED (domestic 8-K/10-K/10-Q filer), PARENT (subsidiary->listed
parent), FOREIGN (US-listed ADR, files 20-F/6-K), DELISTED (was listed; date-dependent), PRIVATE.
confidence: HIGH (unambiguous direct), MED (parent-map or smaller/less-liquid listed — flagged for
review). PRIVATE/generic slugs excluded from matching.
"""
# slug: (company, ticker, CIK, status, confidence)
CROSSWALK = {
 # --- Alphabet ---
 "google":("Alphabet Inc.","GOOGL",1652044,"LISTED","HIGH"),
 "alphabet":("Alphabet Inc.","GOOGL",1652044,"LISTED","HIGH"),
 "youtube":("Alphabet Inc.","GOOGL",1652044,"PARENT","MED"),
 "waymo":("Alphabet Inc.","GOOGL",1652044,"PARENT","MED"),
 "gemini":("Alphabet Inc.","GOOGL",1652044,"PARENT","MED"),
 "google-bard":("Alphabet Inc.","GOOGL",1652044,"PARENT","MED"),
 "google-deepmind":("Alphabet Inc.","GOOGL",1652044,"PARENT","MED"),
 "deepmind":("Alphabet Inc.","GOOGL",1652044,"PARENT","MED"),
 "google-cloud":("Alphabet Inc.","GOOGL",1652044,"PARENT","MED"),
 # --- Meta ---
 "meta":("Meta Platforms, Inc.","META",1326801,"LISTED","HIGH"),
 "facebook":("Meta Platforms, Inc.","META",1326801,"LISTED","HIGH"),
 "instagram":("Meta Platforms, Inc.","META",1326801,"PARENT","MED"),
 "whatsapp":("Meta Platforms, Inc.","META",1326801,"PARENT","MED"),
 "meta-ai":("Meta Platforms, Inc.","META",1326801,"PARENT","MED"),
 # --- Microsoft ---
 "microsoft":("Microsoft Corporation","MSFT",789019,"LISTED","HIGH"),
 "microsoft-copilot":("Microsoft Corporation","MSFT",789019,"PARENT","MED"),
 "microsoft-research":("Microsoft Corporation","MSFT",789019,"PARENT","MED"),
 "bing":("Microsoft Corporation","MSFT",789019,"PARENT","MED"),
 "linkedin":("Microsoft Corporation","MSFT",789019,"PARENT","MED"),
 "github":("Microsoft Corporation","MSFT",789019,"PARENT","MED"),
 # --- Tesla / autos ---
 "tesla":("Tesla, Inc.","TSLA",1318605,"LISTED","HIGH"),
 "cruise":("General Motors Company","GM",1467858,"PARENT","MED"),
 "gm-cruise":("General Motors Company","GM",1467858,"PARENT","MED"),
 "general-motors":("General Motors Company","GM",1467858,"LISTED","HIGH"),
 "zoox":("Amazon.com, Inc.","AMZN",1018724,"PARENT","MED"),
 # --- Amazon / Apple ---
 "amazon":("Amazon.com, Inc.","AMZN",1018724,"LISTED","HIGH"),
 "amazon-web-services":("Amazon.com, Inc.","AMZN",1018724,"PARENT","MED"),
 "aws":("Amazon.com, Inc.","AMZN",1018724,"PARENT","MED"),
 "ring":("Amazon.com, Inc.","AMZN",1018724,"PARENT","MED"),
 "alexa":("Amazon.com, Inc.","AMZN",1018724,"PARENT","MED"),
 "apple":("Apple Inc.","AAPL",320193,"LISTED","HIGH"),
 # --- other listed tech / consumer ---
 "snapchat":("Snap Inc.","SNAP",1564408,"LISTED","HIGH"),
 "snap":("Snap Inc.","SNAP",1564408,"LISTED","HIGH"),
 "uber":("Uber Technologies, Inc.","UBER",1543151,"LISTED","HIGH"),
 "uber-eats":("Uber Technologies, Inc.","UBER",1543151,"PARENT","MED"),
 "lyft":("Lyft, Inc.","LYFT",1759509,"LISTED","HIGH"),
 "netflix":("Netflix, Inc.","NFLX",1065280,"LISTED","HIGH"),
 "nvidia":("NVIDIA Corporation","NVDA",1045810,"LISTED","HIGH"),
 "intel":("Intel Corporation","INTC",50863,"LISTED","HIGH"),
 "ibm":("International Business Machines","IBM",51143,"LISTED","HIGH"),
 "oracle":("Oracle Corporation","ORCL",1341439,"LISTED","HIGH"),
 "salesforce":("Salesforce, Inc.","CRM",1108524,"LISTED","HIGH"),
 "paypal":("PayPal Holdings, Inc.","PYPL",1633917,"LISTED","HIGH"),
 "walmart":("Walmart Inc.","WMT",104169,"LISTED","HIGH"),
 "mcdonald's":("McDonald's Corporation","MCD",63908,"LISTED","HIGH"),
 "mcdonalds":("McDonald's Corporation","MCD",63908,"LISTED","HIGH"),
 "pinterest":("Pinterest, Inc.","PINS",1506293,"LISTED","HIGH"),
 "doordash":("DoorDash, Inc.","DASH",1792789,"LISTED","HIGH"),
 "coinbase":("Coinbase Global, Inc.","COIN",1679788,"LISTED","HIGH"),
 "palantir":("Palantir Technologies Inc.","PLTR",1321655,"LISTED","HIGH"),
 "zillow":("Zillow Group, Inc.","ZG",1617640,"LISTED","HIGH"),
 "shotspotter":("SoundThinking, Inc.","SSTI",1351636,"LISTED","MED"),
 "soundthinking":("SoundThinking, Inc.","SSTI",1351636,"LISTED","MED"),
 "serve-robotics":("Serve Robotics Inc.","SERV",1832483,"LISTED","MED"),
 "integra-lifesciences":("Integra LifeSciences Holdings","IART",917520,"LISTED","MED"),
 "acclarent":("Johnson & Johnson","JNJ",200406,"PARENT","MED"),
 # --- health ---
 "unitedhealth":("UnitedHealth Group Inc.","UNH",731766,"LISTED","HIGH"),
 "unitedhealth-group":("UnitedHealth Group Inc.","UNH",731766,"LISTED","HIGH"),
 "optum":("UnitedHealth Group Inc.","UNH",731766,"PARENT","MED"),
 "navihealth":("UnitedHealth Group Inc.","UNH",731766,"PARENT","MED"),
 "cigna":("The Cigna Group","CI",1739940,"LISTED","HIGH"),
 "humana":("Humana Inc.","HUM",49071,"LISTED","HIGH"),
 # --- finance ---
 "goldman-sachs":("The Goldman Sachs Group Inc.","GS",886982,"LISTED","HIGH"),
 "wells-fargo":("Wells Fargo & Company","WFC",72971,"LISTED","HIGH"),
 "jpmorgan-chase":("JPMorgan Chase & Co.","JPM",19617,"LISTED","HIGH"),
 "jpmorgan":("JPMorgan Chase & Co.","JPM",19617,"LISTED","HIGH"),
 # --- HR / info services ---
 "workday":("Workday, Inc.","WDAY",1327811,"LISTED","HIGH"),
 "thomson-reuters":("Thomson Reuters Corporation","TRI",1075124,"FOREIGN","MED"),
 # --- delisted / status-change (date-dependent) ---
 "rite-aid":("Rite Aid Corporation","RAD",84129,"DELISTED","HIGH"),
 "twitter":("Twitter, Inc.","TWTR",1418091,"DELISTED","HIGH"),
 "x-(twitter)":("X Corp. (fmr Twitter)","TWTR",1418091,"DELISTED","HIGH"),
 "x-corp":("X Corp. (fmr Twitter)","TWTR",1418091,"DELISTED","HIGH"),
 # --- foreign US-listed (ADR / 20-F/40-F; different form set) ---
 "alibaba":("Alibaba Group Holding","BABA",1577552,"FOREIGN","MED"),
 "baidu":("Baidu, Inc.","BIDU",1329099,"FOREIGN","MED"),
 # --- explicit PRIVATE / FOREIGN-private excludes (prevents false flagging) ---
 **{s:("","",None,"PRIVATE","") for s in [
   "openai","anthropic","xai","chatgpt","character.ai","clearview-ai","stability-ai","midjourney",
   "elevenlabs","runway","perplexity","perplexity-ai","mistral","replika","laion","eleutherai",
   "hirevue","proctorio","proctoru","turnitin","gaggle","synthesia","grammarly","inflection",
   "cohere","lensa-ai","faceapp","dataworks-plus","netradyne","omnilert","chai","crushon.ai",
   "nomi-ai","janitorai","you.com","leonardo-ai","anysphere","cursor","deloitte","springer-nature",
   "cnet","state-farm","coco-robotics","quantum-ai","fraudgpt","compvis-lmu"]},
 **{s:("","",None,"FOREIGN","") for s in ["tiktok","bytedance","deepseek","deepseek-ai","huawei",
   "wechat","tencent"]},
}
