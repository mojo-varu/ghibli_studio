# Studio Ghibli Movies

Steps to run the application
1. Install docker and docker-compose on your system, go to https://docs.docker.com/install/
2. Go to the root of the project directory, where `Dockerfile` and `docker-compose.yml` files are located.
3. From root of project directory run `docker-compose build` to build the web application image.
4. Run `docker images ghibli_studio_web` to check newly created image.
5. Then from root of project directory run `docker-compose up`, this will start web app and memecache server.
6. Go to http://localhost:8000/movies/ on your web broswer to get the list of movies.
7. To stop the application, from root of project directory run `docker-compose down`
