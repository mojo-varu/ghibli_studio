# Studio Ghibli Movies

Steps to run the application
1. Install docker and docker-compose on your system, go to https://docs.docker.com/install/
2. Clone the project and checkout to develop branch.
3. Go to root of project directory and run `docker-compose build` to setup the web application image.
4. Run `docker images ghibli_studio_web` to check created image.
5. From root of project, run `docker-compose up`, this will start web app and memecache server.
6. Go to http://localhost:8000/movies/ on your web broswer to get list of movies. :) 
