## Project description
This is a copstone project for advanced track of the Deep Learning School (Fall-2020).
It is a web applocation 

# MM-detect
MMDetection is an open source object detection toolbox based on PyTorch. It comes with a zoo of model prertrained on the [COCO dataset]("https://cocodataset.org/#home").

![appartment](test_images/detected_appartment.jpg)
![diving1](test_images/detected_diving1.jpg)
![diving2](test_images/detected_diving2.jpg)
![zoo](test_images/detected_zoo.jpg)
![park](test_images/detected_park.jpg)
![oval_office](test_images/detected_oval_office.jpg)
![street](test_images/detected_street.jpg)


# Deploymnet om Heroku

heroku container:push web 
heroku container:release web
heroku open

heroku destroy --confirm flask-detector