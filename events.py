from flask_restful import Resource

class Events_data(Resource):
    def get(self):
        return [
        {'id': 0,
         'title': 'Jazz Concert',
         'start_date': '2021-02-14 18:00:00',
         'end_date': '2021-02-14 21:00:00',
         'thumbnail': 'https://media.resources.festicket.com/www/__sized__/photos/1_ZUTKNaz-thumbnail-800x460-90.jpg'
        },
        {'id': 0,
         'title': 'Rock Concert',
         'start_date': '2021-02-13 20:00:00',
         'end_date': '2021-02-13 23:00:00',
         'thumbnail': 'https://d6u22qyv3ngwz.cloudfront.net/ad/7d7W/great-clips-great-haircut-sale-rock-concert-small-5.jpg'
        },
        {'id': 0,
         'title': 'IT Days',
         'start_date': '2021-02-25 09:00:00',
         'end_date': '2021-02-28 18:00:00',
         'thumbnail': 'https://storage.googleapis.com/xmcom-wp-content-uploads/1/2018/1Blog-Thumbnail-341X271@2x-e1543274763520.jpg'
        },
        {'id': 0,
         'title': 'Icecream Workshop',
         'start_date': '2021-02-14 18:00:00',
         'end_date': '2021-02-14 21:00:00',
         'thumbnail': 'https://www.jealousgallery.com/Images/Prints/Dave-Buonaguidi-Have-A-Nice-Day-Ice-Cream-Cones.jpg?Action=thumbnail&Width=500'
        },
        ]
