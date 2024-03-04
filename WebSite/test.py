from intasend import APIService

API_PUBLISHABLE_KEY = 'ISPubKey_test_36e68075-1329-49a4-85c0-4e3df1319d7a'
API_TOKEN= 'ISSecretKey_test_d3f9c963-6aa2-4640-a7c9-673fd004e97a'

service = APIService(token=API_TOKEN,publishable_key=API_PUBLISHABLE_KEY,test=True)

create_orrder = service.collect.mpesa_stk_push(phone_number=25401128793,email='ammodi9@gmail.com',amount=100,narrative='Purchase of items')
print(create_orrder)