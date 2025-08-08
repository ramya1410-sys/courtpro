import requests
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CaseQueryLog
from django.http import JsonResponse
from .captcha_utils import fetch_captcha_code  # adjust path if needed

def get_captcha(request):
    code = fetch_captcha_code()
    if code:
        return JsonResponse({"captcha_code": code})
    else:
        return JsonResponse({"error": "Failed to retrieve CAPTCHA"}, status=500)
@api_view(['POST'])
def fetch_case_data(request):
    # 🌐 Step 1: Get user inputs from frontend
    case_type = request.data.get("case_type")
    case_number = request.data.get("case_number")
    filing_year = request.data.get("filing_year")
    security_code = request.data.get("captcha_input")  # renamed for clarity

    # ✅ Step 2: Prepare payload for POST to court site
    payload = {
        "case_type": case_type,
        "case_no": case_number,
        "case_year": filing_year,
        "security_code": security_code
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://delhihighcourt.nic.in/app/get-case-type-status"

    try:
        # 🔁 Step 3: Send POST request
        res = requests.post(url, data=payload, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        # 🔍 Step 4: Parse case details
        party_tag = soup.select_one(".partyNames")
        filing_tag = soup.select_one("#filingDate")
        hearing_tag = soup.select_one("#nextHearingDate")
        order_tag = soup.select_one("a[href*='.pdf']")

        party_names = party_tag.text.strip() if party_tag else "Not found"
        filing_date = filing_tag.text.strip() if filing_tag else "Not found"
        next_hearing = hearing_tag.text.strip() if hearing_tag else "Not found"
        latest_pdf = order_tag["href"] if order_tag else None

        # 🗂 Step 5: Log query
        CaseQueryLog.objects.create(
            case_type=case_type,
            case_number=case_number,
            filing_year=filing_year,
            raw_html=res.text
        )

        # 📤 Step 6: Return result
        return Response({
            "party_names": party_names,
            "filing_date": filing_date,
            "next_hearing": next_hearing,
            "latest_order_pdf": latest_pdf
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return Response({"error": str(e)}, status=500)
