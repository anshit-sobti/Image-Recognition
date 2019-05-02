# CMPE-266-Project: 
    Image-Recognition using AWS Rekognition

# University Name: 
    [San Jose State University](http://www.sjsu.edu/)

# Course: 
    [CMPE 266 Big Data Engineering and Analytics](http://info.sjsu.edu/web-dbgen/catalog/courses/CMPE266.htmlhttp:// "CMPE 266 Big Data Engineering and Analytics")

# Professor: 
    [Sanjay Garje](https://www.linkedin.com/in/sanjaygarje/ "Sanjay Garje")

# Student: 
    [Kshitij Sood](https://www.linkedin.com/in/soodkshitij/ "Kshitij Sood")

    [Anshit Sobti](https://www.linkedin.com/in/anshitsobti/ "Anshit Sobti")

    [Prajwal Venkatesh](https://www.linkedin.com/in/prajwalvenkatesh/ "Prajwal Venkatesh")

    [Abhineet Gupta](https://www.linkedin.com/in/abhineetgupta1991/ "Abhineet Gupta")

    [Kalikalyan Dash](https://www.linkedin.com/in/dashkk/ "Kalikalyan Dash")
  
# Project Introduction: 
    Image Recognition using AWS Kinesis, Amazon S3, Amazon Rekognition, AWS Lambda, Amazon DynamoDB and Amazon SNS.
	Our application's main focus is to recognize if the image published by the user is similar to the one already saved in our datastore. If they are similar, we will compute the similarity rate and show the similarity percentage by updating the metadata value in a key-value database of the corresponding key.

# Features List:
    The application can automatically analyze streaming data from the Twitter API by using Amazon Kinesis Analytics (Firehose). 
	The analyzed data can then be recognized using Amazon Rekognition based on which we can calculate the similarity between images using Lambda functions.
	Amazon SNS notifies the user when a similar image is found and also provides a similarity percentage.
# Pre-requisites Set Up 
	AWS account - You need to have an aws account to try out this project.
	Create a key pair for ec2
	Create stack using template : https://s3-us-west-1.amazonaws.com/big-data-266project-template-918073364259-us-west-1/template.json
	Enter twitter developer API credentials and select created key pair.
# Start Application:
	Once the stack is created run twitter-streaming.py.
	Send pictures! You can experiment in any way you want. Be sure to mention @Dummy69710367 in your Tweet.
	All images will be logged in DynamoDB, and successful matches will update the DynamoDB record with a match score, and will notify you by email.
    

# Stop Application and Clean-up:
	 Delete the S3 bucket.
	 Delete the CloudFormation stack.
# References
[1] https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-wg.pdf
[2] https://aws.amazon.com/rekognition/
[3] https://aws.amazon.com/lambda/

