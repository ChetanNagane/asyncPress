import csv

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Request, Product
from .tasks import process_images

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')

        if not csv_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'Invalid file format. Please upload a CSV file.'}, status=400)

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)

            header = next(csv_reader)
            if len(header) != 3 or header != ['Serial Number', 'Product Name', 'Input Image Urls']:
                return JsonResponse({'error': 'Invalid CSV format. Headers should be Serial Number,Product Name,Input Image Urls'}, status=400)

            new_request = Request.objects.create()

            for row in csv_reader:
                if len(row) != 3:
                    return JsonResponse({'error': 'Invalid CSV format. Each row must have 3 columns.'}, status=400)

                try:
                    serial_number = int(row[0])
                    product_name = row[1].strip()
                    input_image_urls = row[2].strip()
                except ValueError:
                    return JsonResponse({'error': 'Invalid data type in CSV. Ensure serial numbers are integers.'},
                                        status=400)

                Product.objects.create(
                    request=new_request,
                    serial_number=serial_number,
                    product_name=product_name,
                    input_image_urls=input_image_urls,
                )

            process_images.delay(new_request.request_id)
            return JsonResponse({'request_id': new_request.request_id}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Failed to process CSV: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def check_status(request, request_id):
    try:
        req = Request.objects.get(request_id=request_id)

        response_data = {
            'status': req.status,
        }

        if req.status == 'failed':
            response_data['error_details'] = req.error_details

        return JsonResponse(response_data)

    except Request.DoesNotExist:
        return JsonResponse({'error': 'Request ID not found'}, status=404)



def download_csv(request, request_id):
    try:
        req = Request.objects.get(request_id=request_id)
    except Request.DoesNotExist:
        return HttpResponse('Request ID not found', status=404)
    if req.status in ['failed', 'pending']:
        return HttpResponse(f'Request is/has {req.status}. Can not create CSV.', status=404)
    products = Product.objects.filter(request=req)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="request_{request_id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Serial Number', 'Product Name', 'Input Image Urls', 'Output Image Urls'])

    for index, product in enumerate(products, start=1):
        output_image_urls = product.output_image_urls
        full_output_urls = [request.build_absolute_uri(settings.MEDIA_URL + url.strip()) for url in
                            output_image_urls.split(',')]
        writer.writerow([
            product.serial_number,
            product.product_name,
            product.input_image_urls,
            ','.join(full_output_urls)
        ])

    return response
