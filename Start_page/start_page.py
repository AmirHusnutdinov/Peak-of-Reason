class StartPage:
    def main(self):
        return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
    crossorigin="anonymous">
  <title>Main</title>
</head>
<body>
  <div class="container">
    <a class="btn btn-primary btn-lg" href="http://127.0.0.1:8080/reviews" role="button" >Reviews</a>
    <a class="btn btn-primary btn-lg" href="http://127.0.0.1:8080/events" role="button">Events</a>
    <a class="btn btn-primary btn-lg" href="http://127.0.0.1:8080/blog" role="button">Blog</a>
    <a class="btn btn-primary btn-lg" href="http://127.0.0.1:8080/authorization" role="button">Account</a>
    <a class="btn btn-primary btn-lg" href="http://127.0.0.1:8080/answers" role="button">Answers</a>
    <a class="btn btn-primary btn-lg" href="http://127.0.0.1:8080/about_us" role="button">About</a>
  </div>


</body>
</html>'''
