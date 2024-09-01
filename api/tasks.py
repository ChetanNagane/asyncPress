import os
import requests
from PIL import Image
from io import BytesIO
from celery import shared_task
from .models import Product, Request

@shared_task
def process_images(request_id):
    products = Product.objects.filter(request__request_id=request_id)
    errors = []

    for product in products:
        input_urls = product.input_image_urls.split(',')
        output_urls = []

        for index, url in enumerate(input_urls, 1):
            try:
                response = requests.get(url.strip(), timeout=10)
                response.raise_for_status()

                img = Image.open(BytesIO(response.content))

                img_io = BytesIO()
                img.save(img_io, format='JPEG', quality=50)
                img_io.seek(0)

                output_filename = os.path.join('media', f'{request_id}-{product.id}-{index}.jpeg')
                with open(output_filename, 'wb') as f:
                    f.write(img_io.read())

                output_urls.append(f'{request_id}-{product.id}-{index}.jpeg')
            except requests.exceptions.RequestException as e:
                errors.append(f'Error downloading image from {url}: {str(e)}')
            except (OSError, IOError) as e:
                errors.append(f'Error processing image from {url}: {str(e)}')
            except Exception as e:
                errors.append(f'Unexpected error for {url}: {str(e)}')

        product.output_image_urls = ','.join(output_urls)
        product.save()

    request = Request.objects.get(request_id=request_id)
    if errors:
        request.status = 'failed'
        request.error_details = '\n'.join(errors)  # Assuming `error_details` is a TextField in the Request model
    else:
        request.status = 'completed'
    request.save()
