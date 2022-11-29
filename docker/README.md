### HOW TO RUN DOCKER

  1. open cmd/powershell
  2. git clone (this repo)
  3. cd (this repo)
  4. docker compose up 
  5. open new cmd/powershell
  6. docker build -t "kafkacsv" .
  7. docker run -it --rm kafkacsv python bin/sendStream.py -h
  8. python bin/processStream.py my-stream
  9. open new cmd/powershell
  10. python bin/sendStream.py data/data.xlsx my-stream --speed 10
  11. open browser localhost:3000 for grafana
  12. login grafana user:kafka pass:kafka
  13. in left panel click search symbol you will find 2 dashboard already there
  14. Enjoy!

