from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import csv
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from io import BytesIO




def index(request):
    return render(request,'home.html')


def geocoding_excel(request):

    response=HttpResponse(content_type='text/csv')
    uploaded_file=request.FILES['docs']
    locator = Nominatim(user_agent='mygeocoder')
    geocode = RateLimiter(locator.geocode)
    df=pd.read_excel(uploaded_file)
    df['location'] = df['Address'].apply(geocode)
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)    
    df[['latitude', 'longitude','altitude']]= pd.DataFrame(df['point'].tolist())
    new_df=df[['Address','latitude','longitude']]


    with BytesIO() as b:
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        new_df.to_excel(writer, sheet_name='Sheet1',index=False)
        writer.save()
   

        response = HttpResponse(b.getvalue(),content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Geocoded_%s.xlsx' %(uploaded_file.name[:-4])
        return response