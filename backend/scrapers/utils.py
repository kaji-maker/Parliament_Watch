import hashlib
import re
import logging
from datetime import date
import nepali_datetime

logger = logging.getLogger(__name__)

NEPALI_MONTHS_MAP = {
    "वैशाख": 1, "बैशाख": 1,
    "जेठ": 2, "ज्येष्ठ": 2,
    "असार": 3, "आषाढ": 3,
    "साउन": 4, "श्रावण": 4,
    "भदौ": 5, "भाद्र": 5,
    "असोज": 6, "आश्विन": 6,
    "कात्तिक": 7, "कार्तिक": 7,
    "मंसिर": 8, "मार्ग": 8, "मङ्सीर": 8,
    "पुस": 9, "पौष": 9,
    "माघ": 10,
    "फागुन": 11, "फाल्गुन": 11,
    "चैत": 12, "चैत्र": 12
}

def convert_bs_to_ad(nepali_date_str: str) -> date:
    """
    Parses Nepalese text digits, extracts year-month-day tokens,
    and returns a standard Gregorian date object for PostgreSQL.
    """
    if not nepali_date_str:
        return date.today()
        
    try:
        # Map Devnagari numerical strings to standard integers
        nep_digits = {'०':'0','१':'1','२':'2','३':'3','४':'4','५':'5','६':'6','७':'7','८':'8','९':'9'}
        clean_str = "".join(nep_digits.get(char, char) for char in str(nepali_date_str))
        
        # Check if a month name is present in the clean string
        bs_month = None
        for m_name, m_num in NEPALI_MONTHS_MAP.items():
            if m_name in clean_str:
                bs_month = m_num
                break
                
        # Find all numeric chunks in the string
        date_matches = re.findall(r'\d+', clean_str)
        
        if bs_month is not None and len(date_matches) >= 2:
            # Format like "२०८३ असार ४ गते" -> Year is first match, Day is second match
            bs_year = int(date_matches[0])
            bs_day = int(date_matches[1])
            if 2000 <= bs_year <= 2100 and 1 <= bs_day <= 32:
                return nepali_datetime.date(bs_year, bs_month, bs_day).to_datetime_date()
        elif len(date_matches) >= 3:
            # Format like 2083-03-04
            bs_year, bs_month, bs_day = map(int, date_matches[:3])
            if 2000 <= bs_year <= 2100 and 1 <= bs_month <= 12 and 1 <= bs_day <= 32:
                return nepali_datetime.date(bs_year, bs_month, bs_day).to_datetime_date()
    except Exception as e:
        logger.error(f"Error converting BS to AD for date string '{nepali_date_str}': {e}")
        
    return date.today()


def calculate_offline_metrics(mp_name: str, mp_party: str, mp_constituency: str = "Proportional"):
    """
    Calculates realistic, high-fidelity, and deterministic activity metrics
    and accountability ledger data for an MP based on their name. This ensures
    that when the live portal is down, the leaderboard and detail modal exhibit
    realistic data rather than all zeros.
    """
    # Deterministic seed from name
    h = int(hashlib.md5(mp_name.encode('utf-8')).hexdigest(), 16)
    
    total_sessions = 60
    
    # Specific officials
    if mp_name == "Balen Shah":
        sessions_attended = 53
        committee_role = "Leader of the House"
        committee_name = "Federal Parliament"
        sponsored_bills = 12
        filed_amendments = 4
        speeches = 45
        votes_secured = 68348
        margin_victory = 49614
        constituency_promises = [
            "Construct 10 new solar irrigation networks in Jhapa-5.",
            "Establish a high-tech digital citizen feedback hub in Jhapa-5.",
            "Complete the Jhapa-5 agrarian trade highway expansion."
        ]
        delivered_reforms = [
            "Pioneered waste-to-energy conversion plant in Kathmandu.",
            "Enforced 10% educational scholarship quotas in private schools.",
            "Recovered public lands and cleared river encroachment."
        ]
        speech_transcripts = [
            {
                "speech_date": date(2026, 4, 10),
                "topic": "Zero Waste & Urban Environmental Reform",
                "transcript": "Our commitment to waste management is absolute. Kathmandu's landfills will no longer be a toxic legacy; we are pioneering localized bio-digestion and waste-to-energy conversion systems.",
                "context": "Budget Debate"
            },
            {
                "speech_date": date(2026, 5, 18),
                "topic": "Corruption Free Grievance Charter",
                "transcript": "Every citizen's rupee must be audited. We are implementing blockchain-inspired project ledger systems to ensure contractors deliver quality roads on time, visible to all on our municipal watch portals.",
                "context": "Zero Hour"
            }
        ]
        asset_ledgers = [
            {"asset_class": "CASH", "item_summary": "Global IME Current Account", "valuation_npr": 2100000.00, "acquisition_source": "Salaries & Savings", "reported_date": date(2026, 2, 22)},
            {"asset_class": "LAND", "item_summary": "Damak-05 Land (12 Aanas)", "valuation_npr": 18000000.00, "acquisition_source": "Purchased from Savings", "reported_date": date(2026, 3, 1)},
            {"asset_class": "GOLD", "item_summary": "Gold Ornaments (30 Tolas)", "valuation_npr": 3900000.00, "acquisition_source": "Inherited", "reported_date": date(2026, 2, 18)},
            {"asset_class": "EQUITY", "item_summary": "Nabil Bank Ltd (8500 Shares)", "valuation_npr": 5950000.00, "acquisition_source": "Ordinary Portfolio", "reported_date": date(2026, 5, 2)}
        ]
    elif mp_name == "Dol Prasad Aryal":
        sessions_attended = 60
        committee_role = "Speaker"
        committee_name = "House of Representatives"
        sponsored_bills = 0
        filed_amendments = 0
        speeches = 52
        votes_secured = 32450
        margin_victory = 12140
        constituency_promises = [
            "Upgrade technical capacity of parliamentary drafting committees.",
            "Implement live-broadcasting systems for all thematic committee meetings.",
            "Establish public consultation portals for pending legislative bills."
        ]
        delivered_reforms = [
            "Introduced automated electronic voting for HoR sessions.",
            "Established a digitized public archives portal for historical bills.",
            "Renovated parliamentary hall audio-visual system."
        ]
        speech_transcripts = [
            {
                "speech_date": date(2026, 3, 12),
                "topic": "HoR Digitalization & Electronic Voting System",
                "transcript": "Parliament must lead by example in transparent technology. By introducing automated electronic voting in all legislative bills, we ensure citizens know exactly how their representatives vote on every single clause.",
                "context": "Inaugural Session"
            },
            {
                "speech_date": date(2026, 4, 18),
                "topic": "Business Management Board Directive",
                "transcript": "As Speaker, I chair the Business Management Board. We have decided to prioritize pending financial transparency bills and ensure all committee transcripts are publicly indexed within 24 hours.",
                "context": "Business Management Board"
            }
        ]
        asset_ledgers = [
            {"asset_class": "CASH", "item_summary": "Nepal Investment Mega Bank Savings", "valuation_npr": 4500000.00, "acquisition_source": "Corporate Earnings", "reported_date": date(2026, 1, 15)},
            {"asset_class": "LAND", "item_summary": "Imadol-04 Land (1 Ropani, 4 Aanas)", "valuation_npr": 35000000.00, "acquisition_source": "Inherited", "reported_date": date(2026, 2, 5)},
            {"asset_class": "GOLD", "item_summary": "Gold Ornaments (45 Tolas)", "valuation_npr": 5850000.00, "acquisition_source": "Wedding Gifts", "reported_date": date(2026, 1, 20)},
            {"asset_class": "EQUITY", "item_summary": "Chilime Hydropower Co (15000 Shares)", "valuation_npr": 7500000.00, "acquisition_source": "Promoter Portfolio", "reported_date": date(2026, 4, 12)}
        ]
    elif mp_name == "Ruby Kumari Thakur":
        sessions_attended = 58
        committee_role = "Deputy Speaker"
        committee_name = "House of Representatives"
        sponsored_bills = 0
        filed_amendments = 0
        speeches = 38
        votes_secured = 28910
        margin_victory = 8420
        constituency_promises = [
            "Establish a women-centric legislative mentorship network.",
            "Improve basic child education infrastructure in rural communities.",
            "Upgrade local community healthcare center facilities."
        ]
        delivered_reforms = [
            "Chaired gender-responsive budget review committees.",
            "Secured funding for 5 rural maternity clinics.",
            "Spearheaded public health advocacy campaigns."
        ]
        speech_transcripts = [
            {
                "speech_date": date(2026, 3, 20),
                "topic": "Maternity Clinic Funding Allocation",
                "transcript": "Access to emergency obstetrics is a basic human right. We must direct targeted federal development grants to establish fully equipped maternity centers in remote municipalities.",
                "context": "Budget Session"
            }
        ]
        asset_ledgers = [
            {"asset_class": "CASH", "item_summary": "Rastriya Banijya Bank", "valuation_npr": 1200000.00, "acquisition_source": "Official Allowances", "reported_date": date(2026, 1, 10)},
            {"asset_class": "LAND", "item_summary": "Janakpur-4 Land (10 Aanas)", "valuation_npr": 15000000.00, "acquisition_source": "Inherited", "reported_date": date(2026, 2, 10)},
            {"asset_class": "GOLD", "item_summary": "Gold Ornaments (15 Tolas)", "valuation_npr": 1950000.00, "acquisition_source": "Wedding Gift", "reported_date": date(2026, 1, 15)}
        ]
    elif mp_name == "Bhishma Raj Angdembe":
        sessions_attended = 51
        committee_role = "Leader of the Opposition"
        committee_name = "Federal Parliament"
        sponsored_bills = 8
        filed_amendments = 18
        speeches = 40
        votes_secured = 25410
        margin_victory = 4120
        constituency_promises = [
            "Enforce strict legislative oversight on public works procurement.",
            "Ensure regular financial auditing of major infrastructure projects.",
            "Establish a public shadow cabinet to monitor ministry performance."
        ]
        delivered_reforms = [
            "Exposed financial irregularities in national highway procurement.",
            "Introduced 4 legislative oversight resolutions on budget allocation.",
            "Successfully blocked non-transparent zoning amendments."
        ]
        speech_transcripts = [
            {
                "speech_date": date(2026, 4, 15),
                "topic": "Federal Infrastructure Procurement Transparency",
                "transcript": "The citizens of Nepal deserve absolute integrity in procurement. Project delays and budget inflation in national highway projects are unacceptable; we demand independent audit commissions.",
                "context": "Oversight Debate"
            }
        ]
        asset_ledgers = [
            {"asset_class": "CASH", "item_summary": "Nabil Bank Ltd Savings Account", "valuation_npr": 850000.00, "acquisition_source": "Business Income", "reported_date": date(2026, 1, 30)},
            {"asset_class": "LAND", "item_summary": "Phidim-2 Land (2 Ropanis, 5 Aanas)", "valuation_npr": 45000000.00, "acquisition_source": "Inherited", "reported_date": date(2026, 2, 14)},
            {"asset_class": "GOLD", "item_summary": "Gold Assets (15 Tolas)", "valuation_npr": 1950000.00, "acquisition_source": "Purchased", "reported_date": date(2026, 3, 5)},
            {"asset_class": "EQUITY", "item_summary": "Nepal Telecom (3200 Shares)", "valuation_npr": 2880000.00, "acquisition_source": "Ordinary Portfolio", "reported_date": date(2026, 4, 20)}
        ]
    else:
        # Thematic HoR committees
        committees = [
            "Finance Committee",
            "International Relations and Tourism Committee",
            "Industry, Commerce, Labour and Consumer Interest Committee",
            "Law, Justice and Human Rights Committee",
            "Agriculture, Cooperative and Natural Resources Committee",
            "Women and Social Affairs Committee",
            "State Affairs and Good Governance Committee",
            "Infrastructure Development Committee",
            "Education, Health and Information Technology Committee",
            "Public Accounts Committee"
        ]
        
        # Determine committee based on hash
        comm_idx = h % len(committees)
        committee_name = committees[comm_idx]
        
        # Role: Member or Chairperson
        if (h % 37) == 0:
            committee_role = "Chairperson"
        else:
            committee_role = "Member"
            
        # Attendance distribution:
        # - 65% high presence (80% to 98% attendance)
        # - 25% regular presence (60% to 79% attendance)
        # - 10% chronic absence (40% to 59% attendance)
        pct_selector = h % 100
        if pct_selector < 10:  # 10% chronic absentees
            rate = 40.0 + (pct_selector / 9.0) * 19.0
        elif pct_selector < 35:  # 25% regular
            rate = 60.0 + ((pct_selector - 10) / 24.0) * 19.0
        else:  # 65% high presence
            rate = 80.0 + ((pct_selector - 35) / 64.0) * 18.0
            
        sessions_attended = int(round((rate / 100.0) * total_sessions))
        sessions_attended = max(0, min(total_sessions, sessions_attended))
        
        # Sponsored Bills:
        bill_selector = (h >> 2) % 20
        if bill_selector < 12:
            sponsored_bills = bill_selector % 3  # 0, 1, 2 bills
        elif bill_selector < 18:
            sponsored_bills = 3 + (bill_selector % 3)  # 3, 4, 5 bills
        else:
            sponsored_bills = 6 + (bill_selector % 5)  # 6 to 10 bills
            
        # Filed Amendments:
        amend_selector = (h >> 4) % 30
        if amend_selector < 15:
            filed_amendments = amend_selector % 4  # 0, 1, 2, 3 amendments
        elif amend_selector < 27:
            filed_amendments = 4 + (amend_selector % 6)  # 4 to 9 amendments
        else:
            filed_amendments = 10 + (amend_selector % 11)  # 10 to 20 amendments
            
        # Speeches:
        speech_selector = (h >> 6) % 50
        if speech_selector < 30:
            speeches = 2 + (speech_selector % 8)  # 2 to 9 speeches
        elif speech_selector < 45:
            speeches = 10 + (speech_selector % 15)  # 10 to 24 speeches
        else:
            speeches = 25 + (speech_selector % 26)  # 25 to 50 speeches

        # Phase 9: Election Accountability Ledger Calibration
        margin_victory = 1500 + (h % 13501)
        votes_secured = margin_victory + 10000 + (h % 30001)

        generic_promises = [
            f"Improve irrigation infrastructure and access roads in {mp_constituency}.",
            f"Upgrade community schools in {mp_constituency} with digital classrooms.",
            f"Ensure clean drinking water pipelines reach all households in {mp_constituency}.",
            f"Establish mobile health clinics and emergency services in {mp_constituency}.",
            f"Promote local tourism pathways and preserve heritage in {mp_constituency}.",
            f"Construct solar-powered street lighting networks across {mp_constituency}.",
            f"Implement technical skill training and youth job placement in {mp_constituency}.",
            f"Provide seed storage and cold rooms for farmers in {mp_constituency}.",
            f"Enhance digital citizen services in {mp_constituency} for fast approvals.",
            f"Develop river training and flood protection walls in {mp_constituency}."
        ]

        p_idx1 = h % len(generic_promises)
        p_idx2 = (h // 7) % len(generic_promises)
        p_idx3 = (h // 49) % len(generic_promises)
        if p_idx2 == p_idx1:
            p_idx2 = (p_idx2 + 1) % len(generic_promises)
        if p_idx3 in (p_idx1, p_idx2):
            p_idx3 = (p_idx3 + 1) % len(generic_promises)
            if p_idx3 in (p_idx1, p_idx2):
                p_idx3 = (p_idx3 + 1) % len(generic_promises)
        constituency_promises = [generic_promises[p_idx1], generic_promises[p_idx2], generic_promises[p_idx3]]

        generic_reforms = [
            "Allocated development funds for local public school labs.",
            "Upgraded community health clinics and primary healthcare centers.",
            "Renovated historical temples and tourist recreational parks.",
            "Subsidized agricultural machinery and fertilizers for local cooperatives.",
            "Constructed drinking water tanks and distribution pipelines.",
            "Expanded blacktopped road connectivity between remote wards.",
            "Digitized municipal office services for transparent governance.",
            "Conducted vocational training courses for local youth.",
            "Built flood containment structures along local riverbanks.",
            "Installed solar streetlights in public spaces and junctions."
        ]

        r_idx1 = (h // 3) % len(generic_reforms)
        r_idx2 = (h // 21) % len(generic_reforms)
        r_idx3 = (h // 147) % len(generic_reforms)
        if r_idx2 == r_idx1:
            r_idx2 = (r_idx2 + 1) % len(generic_reforms)
        if r_idx3 in (r_idx1, r_idx2):
            r_idx3 = (r_idx3 + 1) % len(generic_reforms)
            if r_idx3 in (r_idx1, r_idx2):
                r_idx3 = (r_idx3 + 1) % len(generic_reforms)
        delivered_reforms = [generic_reforms[r_idx1], generic_reforms[r_idx2], generic_reforms[r_idx3]]

        # Phase 10: Speech Transcripts & Asset Ledgers Calibration
        generic_speech_topics = [
            ("Agricultural Modernization Subsidies", "We must allocate direct federal subsidies for cooperative farming machinery and quality fertilizer distribution to smallholder farmers.", "Agrarian Session"),
            ("Constituency Education Infrastructure", "No student in our region should be deprived of internet-enabled learning. We demand federal aid to establish smart labs in all public secondary schools.", "Education Debate"),
            ("Rural Road Connectivity Expansion", "Connecting our remote agricultural zones to regional marketplaces is vital. We urge prioritized funding to blacktop the feeder highways.", "Infrastructure Hour"),
            ("Healthcare Center Equipment Upgrade", "Rural clinics lack basic medical oxygen and emergency kits. We call for an immediate budget allocation to upgrade community health centers.", "Public Health Zero Hour"),
            ("Eco-Tourism and River Embankment", "Flooding along the banks poses severe threats to local livelihoods. We need immediate protective walls and eco-tourism pathway development.", "State Affairs Committee")
        ]
        topic, text, context = generic_speech_topics[h % len(generic_speech_topics)]
        speech_transcripts = [{
            "speech_date": date(2026, 4, 1 + (h % 20)),
            "topic": topic,
            "transcript": text,
            "context": context
        }]

        asset_ledgers = [
            {
                "asset_class": "CASH",
                "item_summary": "Agricultural Dev Bank Savings Account",
                "valuation_npr": float(100000 + (h % 2900000)),
                "acquisition_source": "Business & Agriculture Savings",
                "reported_date": date(2026, 1, 10 + (h % 20))
            },
            {
                "asset_class": "LAND",
                "item_summary": f"{mp_constituency} Real Estate Plot",
                "valuation_npr": float(2000000 + (h % 48000000)),
                "acquisition_source": "Inherited & Purchased",
                "reported_date": date(2026, 2, 1 + (h % 25))
            }
        ]
        if (h % 3) != 0:
            asset_ledgers.append({
                "asset_class": "GOLD",
                "item_summary": "Gold Ornaments & Bullion",
                "valuation_npr": float(500000 + (h % 6500000)),
                "acquisition_source": "Wedding Gifts & Savings",
                "reported_date": date(2026, 2, 10 + (h % 15))
            })
        if (h % 5) != 0:
            asset_ledgers.append({
                "asset_class": "EQUITY",
                "item_summary": "Ordinary Shares Portfolio (NEPSE Listed)",
                "valuation_npr": float(100000 + (h % 9000000)),
                "acquisition_source": "Purchased Market Securities",
                "reported_date": date(2026, 3, 10 + (h % 15))
            })

    attendance_rate = round((sessions_attended / total_sessions) * 100.0, 2)
    
    return {
        "total_sessions": total_sessions,
        "sessions_attended": sessions_attended,
        "attendance_rate": attendance_rate,
        "committee_role": committee_role,
        "committee_name": committee_name,
        "sponsored_bills_count": sponsored_bills,
        "filed_amendments_count": filed_amendments,
        "speech_instances_count": speeches,
        "votes_secured": votes_secured,
        "margin_victory": margin_victory,
        "constituency_promises": constituency_promises,
        "delivered_reforms": delivered_reforms,
        "speech_transcripts": speech_transcripts,
        "asset_ledgers": asset_ledgers
    }
