from aiohttp import ClientSession, ClientResponseError, ClientError


class Database:
    base_url = "https://zahraton.itlink.uz/api"
    # base_url = "http://localhost:8000/api"
    cashbek_url = "https://cabinet.cashbek.uz/services/gocashapi/api"

    async def make_request(self, method, endpoint, data=None):
        url = self.base_url + endpoint

        try:
            async with ClientSession() as session:
                async with session.request(method, url, json=data) as resp:
                    # r = await resp.json()

                    # logging.info(r)
                    if resp.status in [200, 201]:
                        x = await resp.json()

                        return x, resp.status
                    else:
                        x = await resp.json()
                        raise ClientResponseError(resp.request_info,
                                                  resp.history,
                                                  status=resp.status,
                                                  message=resp.reason)
        except ClientError as e:
            raise e
        finally:
            await session.close()

    async def get_user(self, user_id):
        user = await self.make_request("GET", f"/get_user/?user_id={user_id}")
        if user and user[1] == 200:
            return user[0]
        return None

    async def get_news(self, user_id):
        return await self.make_request("GET", f"/news/?user_id={user_id}")

    async def get_active_sales_all(self):
        return await self.make_request("GET", "/sales/")

    async def add_chat(self, user_id):
        return await self.make_request("POST", "/add_chat/",
                                       {'user_id': user_id}
                                       )

    async def add_user(self, phone, name, telegram_id, gender, latitude, longitude, birth, uuid=None):
        async with ClientSession() as session:
            data = {
                'phone': phone,
                'telegram_id': telegram_id,
                'full_name': name,
                'gender': gender,
                'latitude': latitude,
                'longitude': longitude,
                'birth': birth,
            }
            async with session.request("POST", self.base_url + "/post_user/", json=data) as resp:
                x = await resp.json()
                return x

    async def register_new_user(self, gender, phone, name, user_id, longitude, latitude, birth):
        data = {
            "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
            "phone": phone,
            "firstName": name,
            "lastName": "NN",
            "gender": "1" if '👩‍💼 Ayollar uchun' in gender else "0",
            "birthDate": birth
        }
        async with ClientSession() as session:
            async with session.request("POST", self.cashbek_url + "/register-client", json=data) as _resp:
                payload = {
                    "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
                    "phone": phone
                }
                async with session.request("POST", self.cashbek_url + "/get-uuid", json=payload) as resp:
                    response = await resp.json()
                    if resp.status == 200 and 'userUUID' in response:
                        user = await self.add_user(name=name, phone=phone, telegram_id=user_id, gender=gender,
                                                   longitude=longitude,
                                                   latitude=latitude, birth=birth)
                        return user
                    else:
                        return None

    async def get_api_uuid(self, phone):
        async with ClientSession() as session:
            payload = {
                "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
                "phone": phone
            }
            async with session.request("POST", self.cashbek_url + "/get-uuid", json=payload) as resp:
                x = await resp.json()
                if resp.status == 200 and 'userUUID' in x:
                    return x["userUUID"]

    async def get_user_balance(self, phone):
        user_uuid = await self.get_api_uuid(phone)
        async with ClientSession() as session:
            payload = {
                "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
                "clientCode": int(user_uuid)
            }
            async with session.request("POST", self.cashbek_url + "/get-user-balance", json=payload) as resp:
                x = await resp.json()
                return x

    async def get_user_orders(self, phone, page=None):
        keys = ['e67ab364-bc13-11ec-8a51-0242ac12000d', 'e67ab364-bc13-11ec-8a51-0242ac12000d',
                '340c3b26-59ac-11ed-91c5-0242ac12000f', 'b97c33b0-40e8-11ed-9ade-0242ac120008']
        orders = []
        for key in keys:
            async with ClientSession() as session:
                payload = {
                    "key": key,
                    "phone": phone
                }
                async with session.request("POST", self.cashbek_url + "/cheque-pageList", json=payload) as resp:
                    x = await resp.json()
                    orders += x
        return orders

    async def get_order_month(self, phone, year):
        data = await self.get_user_orders(phone=phone)
        months = set()
        for obj in data:
            cheque_date = obj['chequeDate']
            order_year = cheque_date[:4]
            if order_year == year:
                month = cheque_date[5:7]
                months.add(month)
        return list(months)

    async def get_orders_by_month(self, phone, year, month):
        data = await self.get_user_orders(phone=phone)
        orders = []
        for obj in data:
            cheque_date = obj['chequeDate']
            order_year = cheque_date[:4]
            order_month = cheque_date[5:7]
            if year == order_year and month == order_month:
                orders.append(obj)
        return orders
