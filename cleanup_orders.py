from api.api_client import APIClient

client = APIClient()
tracks = [
    232309, 93419, 58461, 824693, 573766, 335616, 661532,
    14701, 268213, 898237, 498952,
    899288, 584637, 201472, 353739, 827816, 455986,
    87711, 903145, 312126, 978501, 397089,
]
for track in tracks:
    r = client.cancel_order(track)
    print(track, r.status_code)

