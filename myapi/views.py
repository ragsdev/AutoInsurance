import string

from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Claims
from .serializers import ClaimsSerializer
from rest_framework.decorators import api_view
from datetime import datetime, date
# import calendar
from . import constants


def check_age(birth_date):
    todays_date = date.today()
    birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
    current_age = (todays_date.year - birth_date_obj.year)
    if current_age < 18:
        return True
    else:
        return False


def get_current_age(birth_date):
    todays_date = date.today()
    birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
    current_age = (todays_date.year - birth_date_obj.year)
    return current_age


def check_if_sunday(p_date):
    created_date_obj = datetime.strptime(p_date, '%Y-%m-%d')
    currweekday = created_date_obj.weekday()
    if currweekday == 6:
        return True
    else:
        return False


def validate_vehicle(veh_type):
    list_of_vehicles={"car", "lorry", "bike", "scooter", "bus"}
    #if veh_type in list_of_vehicles:
    #    return False
    #else:
    #    return True
    #if veh_type.upper() in (name.upper() for name in list_of_vehicles): #will work for both upper, lower case and upper lower case mixed words
    if veh_type.lower() in list_of_vehicles: #will work for both upper, lower case and upper lower case mixed words
        return False
    else:
        return True

def validate_license_num(l_num):
    if len(l_num) == 7 and l_num.digits:
        return False
    else:
        return True



@api_view(['POST'])
def submit_claims(request):
    if request.method == 'POST':
        claims_data = JSONParser().parse(request)

        if (int(claims_data['claims_amount']) < 1000) or (int(claims_data['claims_amount']) > 50000):
            print(claims_data['claims_amount'])
            # return JsonResponse({'message': "Invalid claim amount"}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'message': constants.INVALID_CLAIM_AMOUNTS}, status=status.HTTP_404_NOT_FOUND)

        # birth_date_str = claims_data['birth_date']
        # birth_date_obj = datetime.strptime(birth_date_str, '%d/%m/%Y')
        # current_age=(todays_date.year - birth_date_obj.year)

        birth_date_str = claims_data['birth_date']
        current_age = get_current_age(birth_date_str)

        #print(check_age(birth_date_str))
        if check_age(birth_date_str):
            print(claims_data['birth_date'])
            # return JsonResponse({'message': "Age should be greater than 18"}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'message': constants.AGE_SHOULD_BE_ABOVE_EIGHTEEN}, status=status.HTTP_404_NOT_FOUND)

        created_date_str = claims_data['created_date']
        if check_if_sunday(created_date_str):
            return JsonResponse({'message': constants.CANNOT_SUBMIT_ON_SUNDAYS}, status=status.HTTP_404_NOT_FOUND)

        new_date_str = claims_data['created_date']
        new_date_obj = datetime.strptime(new_date_str, '%Y-%m-%d')

        # current_date = new_date_obj.weekday()
        # if (current_date == 6):
        #    print(current_date)
        # return JsonResponse({'message': "cannot submit on Sunday"}, status=status.HTTP_404_NOT_FOUND)
        #   return JsonResponse({'message': constants.CANNOT_SUBMIT_ON_SUNDAY}, status=status.HTTP_404_NOT_FOUND)
        # current_date = today_date_obj.weekday()

        if new_date_obj.date() > datetime.date(datetime.now()):
            # return JsonResponse({'message': "Cannot submit a claim for future date"},
            # status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'message': constants.CANNOT_SUBMIT_FOR_FUTURE_DATE}, status=status.HTTP_404_NOT_FOUND)

        type = claims_data['vehicle_type']
        print(validate_vehicle(type))
        if validate_vehicle(type):
            return JsonResponse({'message': constants.CANNOT_SUBMIT_VEHICLE}, status=status.HTTP_404_NOT_FOUND)

        license_number = claims_data['license_num']
        print(validate_license_num(license_number))
        if validate_license_num(license_number):
            return JsonResponse({'message': constants.INVALID_lICENSE_NUM}, status=status.HTTP_404_NOT_FOUND)

        model_data = dict(name=claims_data['name'], age=current_age, address=claims_data['address'],
                          license_num=claims_data['license_num'], id_proof=claims_data['id_proof'],
                          claims_amount=claims_data['claims_amount'], created_date=claims_data['created_date'],
                          vehicle_type=claims_data['vehicle_type'])
        claims_serializer = ClaimsSerializer(data=model_data)

        if claims_serializer.is_valid():
            claims_serializer.save()
            return JsonResponse(claims_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(claims_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def claims_list(request):
    if request.method == 'GET':
        claims = Claims.objects.all()
        claims_serializer = ClaimsSerializer(claims, many=True)
        return JsonResponse(claims_serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def claims_by_id(request, cid):
    claims = Claims.objects.filter(id=cid)
    if not claims.exists():
        error_message = "The claim no {scid} does not exist".format(scid=cid)
        return JsonResponse({'message': error_message}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        claims_serializer = ClaimsSerializer(claims, many=True)
        return JsonResponse(claims_serializer.data, safe=False)

    elif request.method == 'PUT':
        try:
            claims = Claims.objects.get(id=cid)
        except Claims.DoesNotExist:
            error_message = "The claim no {scid} does not exist".format(scid=cid)
            return JsonResponse({'message': error_message}, status=status.HTTP_404_NOT_FOUND)

        claims_data = JSONParser().parse(request)
        claims_serializer = ClaimsSerializer(claims, data=claims_data)
        if claims_serializer.is_valid():
            claims_serializer.save()
            return JsonResponse(claims_serializer.data)
        return JsonResponse(claims_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        claims.delete()
        error_message = "The claim no {scid} was deleted successfully".format(scid=cid)
        return JsonResponse({'message': error_message}, status=status.HTTP_204_NO_CONTENT)

