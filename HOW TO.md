# Running Kafka for the given CDN dataset

## Kafka 
1. Installation

Run the related kafka containers using *docker-compose*, execute the following command from this directory:

        docker-compose up -d
	
	docker build -t "kafkacsv" .
	docker run -it --rm kafkacsv python bin/sendStream.py -h
	
Data:

	- Add the Excel file to the ./docker/data directory

2. Consumer 

open a terminal, run this consumer to receive and read the streamed data in the topic "my-stream", if topic doesn't exist it will be created automatically:
		
        python /docker/bin/processStream.py my-stream
	
To run the sketches, run the following command:

	python /sketches/<sketch_name>.py my-stream
	
3. Producer

The Kafka Producer has the role to turn the Excil file into streamed data and send it to a consumer where the sketches will be implemented later.
	
From this directory the following command can be used to run the producer:

        python /docker/bin/sendStream.py [Path to the Excil File] [Name of the Kafka topic] [Optional: Multiplying factor for the sending speed]
		
Therefore, to launch a producer for our dataset (in actual speed):
        
        python /docker/bin/sendStream.py "/data/data/data.xlsx" my-stream 
		
It is also possible to add a third argue to specify a multiplying factor to the speed. For example to multiply the speed by 1000 (compared to the original timestamp) the following command should be used:

        python /docker/bin/sendStream.py "/docker/data/<file_name>.xlsx" my-stream --speed 10
	
	
4. Grafana

		open browser localhost:3000 for grafana
	
		login grafana user:kafka pass:kafka
	
		in left panel click search symbol you will find 2 dashboard already there
	
Enjoy!
		

	
