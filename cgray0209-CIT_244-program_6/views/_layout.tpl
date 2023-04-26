<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
            rel="stylesheet"
            integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65"
            crossorigin="anonymous"
        />
        <title>WXYZ Corp{{ f" | {page_title}" if page_title else "" }}</title>
    </head>

    <body class="container">
        <header>
            <nav class="navbar navbar-expand-sm navbar-light mb-4 bg-light">
                <div class="container">
                    <a class="navbar-brand" href="/">WXYZ Corp</a>
                    <button
                        class="navbar-toggler d-lg-none"
                        data-bs-target="#navbarSupportedContent"
                        data-bs-toggle="collapse"
                        type="button"
                        aria-controls="navbarSupportedContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                    >
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="navbar-collapse collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav mt-2 mt-lg-0 me-auto">
                            <li class="nav-item">
                                <a class="nav-link" href="/" aria-current="page"
                                    >Home <span class="visually-hidden">(current)</span></a
                                >
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/list-by-department"
                                    >View by Department</a
                                >
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/update-hours">Edit Employee Data</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
        <main>
            <h1 class="pb-4 px-4 my-4 border-bottom">{{ page_heading }}</h1>
            {{ !base }}
        </main>
        <footer
            class="d-flex flex-wrap align-items-center justify-content-between py-3 my-3 border-top"
        >
            <div
                class="d-flex align-items-center justify-content-center justify-content-sm-start col-12 col-sm-4"
            >
                <small class="mb-3 mb-md-0 text-muted">Copyright © 2023 Chet Gray</small>
            </div>
            <div
                class="d-flex align-items-center justify-content-center justify-content-sm-end col-12 col-sm-4"
            >
                <small class="text-muted">We know what we're doing.</small>
            </div>
        </footer>
        <script
            src="https://code.jquery.com/jquery-3.6.3.min.js"
            integrity="sha256-pvPw+upLPUjgMXY0G+8O0xUf+/Im1MZjXxxgOcBQBXU="
            crossorigin="anonymous"
        ></script>
        <script
            src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4"
            crossorigin="anonymous"
        ></script>
    </body>
</html>
