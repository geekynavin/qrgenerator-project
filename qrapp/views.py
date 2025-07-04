import qrcode
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
import base64

def index(request):
    qr_code = None
    qr_data = None

    if request.method == "POST":
        qr_data = request.POST.get("qrdata")
        img = qrcode.make(qr_data)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        qr_code = f'data:image/png;base64,{img_base64}'

    return render(request, 'qrapp/index.html', {'qr_code': qr_code, 'qr_data': qr_data})

def download_qr(request):
    data = request.GET.get("data")
    if not data:
        return HttpResponse("No data provided.", status=400)

    img = qrcode.make(data)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png', headers={
        'Content-Disposition': 'attachment; filename="qr_code.png"',
    })
