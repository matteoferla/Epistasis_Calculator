<!DOCTYPE html>
<html lang="en">

    <head>
        <%include file="google_analytics.mako"/>
        <meta charset="UTF-8">
        <meta name="description" content="Epistasis calculator">
        <meta name="author" content="Matteo Ferla 2020">
        <title>Epistasis</title>
        <!-- Bootstrap 4 core CSS-->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
        <link rel="stylesheet" href="https://www.matteoferla.com/Font-Awesome-Pro/css/all.min.css" crossorigin="anonymous">
        <!-- Twitter -->
        <meta name="twitter:card" content="summary">
        <meta property="og:title" content="Epistasis calculator">
        <meta property="og:description" content="Epistasis calculator">
        <meta property="og:url" content="epistasis.mutanalyst.com">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
    <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
    <script src="https://code.jquery.com/jquery-3.3.1.js" integrity="sha256-2Kok7MbOyxpgUVvAk/HJ2jigOSYS2auK4Pfzbm7uH60="
            crossorigin="anonymous"></script>
        <style>
            .table input {
                display:block;
                width:80%;
                margin-left:auto;
                margin-right:auto;
            }
            div.tooltip {
                position: absolute;
                text-align: center;
                width: 60px;
                height: 28px;
                padding: 2px;
                font: 12px sans-serif;
                background: lightsteelblue;
                border: 0px;
                border-radius: 8px;
                pointer-events: none;
            }
            body {
                background-color: #dedede;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' width='46' height='23' viewBox='0 0 46 23'%3E%3Cdefs%3E%3Crect stroke='%23dedede' stroke-width='0.1' width='1' height='1' id='s'/%3E%3Cpattern id='a' width='2' height='2' patternUnits='userSpaceOnUse'%3E%3Cg stroke='%23dedede' stroke-width='0.1'%3E%3Crect fill='%23dadada' width='1' height='1'/%3E%3Crect fill='%23dedede' width='1' height='1' x='1' y='1'/%3E%3Crect fill='%23d5d5d5' width='1' height='1' y='1'/%3E%3Crect fill='%23d1d1d1' width='1' height='1' x='1'/%3E%3C/g%3E%3C/pattern%3E%3Cpattern id='b' width='5' height='11' patternUnits='userSpaceOnUse'%3E%3Cg fill='%23cccccc'%3E%3Cuse xlink:href='%23s' x='2' y='0'/%3E%3Cuse xlink:href='%23s' x='4' y='1'/%3E%3Cuse xlink:href='%23s' x='1' y='2'/%3E%3Cuse xlink:href='%23s' x='2' y='4'/%3E%3Cuse xlink:href='%23s' x='4' y='6'/%3E%3Cuse xlink:href='%23s' x='0' y='8'/%3E%3Cuse xlink:href='%23s' x='3' y='9'/%3E%3C/g%3E%3C/pattern%3E%3Cpattern id='c' width='7' height='7' patternUnits='userSpaceOnUse'%3E%3Cg fill='%23c8c8c8'%3E%3Cuse xlink:href='%23s' x='1' y='1'/%3E%3Cuse xlink:href='%23s' x='3' y='4'/%3E%3Cuse xlink:href='%23s' x='5' y='6'/%3E%3Cuse xlink:href='%23s' x='0' y='3'/%3E%3C/g%3E%3C/pattern%3E%3Cpattern id='d' width='11' height='5' patternUnits='userSpaceOnUse'%3E%3Cg fill='%23dedede'%3E%3Cuse xlink:href='%23s' x='1' y='1'/%3E%3Cuse xlink:href='%23s' x='6' y='3'/%3E%3Cuse xlink:href='%23s' x='8' y='2'/%3E%3Cuse xlink:href='%23s' x='3' y='0'/%3E%3Cuse xlink:href='%23s' x='0' y='3'/%3E%3C/g%3E%3Cg fill='%23c3c3c3'%3E%3Cuse xlink:href='%23s' x='8' y='3'/%3E%3Cuse xlink:href='%23s' x='4' y='2'/%3E%3Cuse xlink:href='%23s' x='5' y='4'/%3E%3Cuse xlink:href='%23s' x='10' y='0'/%3E%3C/g%3E%3C/pattern%3E%3Cpattern id='e' width='47' height='23' patternUnits='userSpaceOnUse'%3E%3Cg fill='%23b54747'%3E%3Cuse xlink:href='%23s' x='2' y='5'/%3E%3Cuse xlink:href='%23s' x='23' y='13'/%3E%3Cuse xlink:href='%23s' x='4' y='18'/%3E%3Cuse xlink:href='%23s' x='35' y='9'/%3E%3C/g%3E%3C/pattern%3E%3Cpattern id='f' width='61' height='31' patternUnits='userSpaceOnUse'%3E%3Cg fill='%2347b56d'%3E%3Cuse xlink:href='%23s' x='16' y='0'/%3E%3Cuse xlink:href='%23s' x='13' y='22'/%3E%3Cuse xlink:href='%23s' x='44' y='15'/%3E%3Cuse xlink:href='%23s' x='12' y='11'/%3E%3C/g%3E%3C/pattern%3E%3C/defs%3E%3Crect fill='url(%23a)' width='46' height='23'/%3E%3Crect fill='url(%23b)' width='46' height='23'/%3E%3Crect fill='url(%23c)' width='46' height='23'/%3E%3Crect fill='url(%23d)' width='46' height='23'/%3E%3Crect fill='url(%23e)' width='46' height='23'/%3E%3Crect fill='url(%23f)' width='46' height='23'/%3E%3C/svg%3E");
                background-attachment: fixed;
                background-size: cover;
            }
        </style>
    </head>

    <body class="bg-light">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top navbar-expand-md"> <a class="navbar-brand" href="#">Epistasis calculator</a>
            <button class="navbar-toggler"
            type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown"
            aria-expanded="false" aria-label="Toggle navigation"> <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav">
                    <li class="nav-item"> <a class="nav-link" href="https://www.biorxiv.org/content/10.1101/2020.04.14.041590v1" target="_blank" ><i class="far fa-book"></i> Underlying paper</a>
                    </li>
                    <li class="nav-item"> <a class="nav-link" href="#" id="mail"><i class="far fa-envelope"></i> Contact us</a>
                        <!--
                        filled dynamically-->
                    </li>
                    <li class="nav-item dropdown"> <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink"
                        data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">

                    <i class="far fa-feather-alt"></i> Authors' Homepages
                </a>
                        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                            <a class="dropdown-item" href="https://scholar.google.com/citations?user=yZDS88IAAAAJ" target="_blank"><i class="far fa-graduation-cap"></i> Carlos G. Acevedo-Rocha</a>
                            <a class="dropdown-item" href="https://scholar.google.com/" target="_blank"><i class="far fa-flask"></i> Aitao Li</a>
                            <a class="dropdown-item" href="https://scholar.google.com/" target="_blank"><i class="far fa-graduation-cap"></i> Lorenzo D’Amore</a>
                            <a class="dropdown-item" href="https://scholar.google.com/" target="_blank"><i class="far fa-vials"></i> Sabrina Hoebenreich</a>
                            <a class="dropdown-item" href="https://scholar.google.com/" target="_blank"><i class="far fa-chart-network"></i> Joaquin Sanchis</a>
                            <a class="dropdown-item" href="https://www.researchgate.net/profile/Paul_Lubrano" target="_blank"><i class="far fa-code"></i> Paul Lubrano</a>
                            <a class="dropdown-item" href="https://www.matteoferla.com" target="_blank"><i class="far fa-globe"></i> Matteo P. Ferla</a>
                            <a class="dropdown-item" href="https://mgarciaborras.wordpress.com/" target="_blank"><i class="far fa-camcorder"></i> Marc Garcia-Borràs</a>
                            <a class="dropdown-item" href="https://silviaosuna.wordpress.com/" target="_blank"><i class="far fa-camera-movie"></i> Sílvia Osuna</a>
                            <a class="dropdown-item" href="https://www.kofo.mpg.de/en/research/biocatalysis" target="_blank"><i class="far fa-graduation-cap"></i> Manfred T. Reetz</a>
                        </div>
                    </li>
                    <li class="nav-item"> <a class="nav-link" href="https://github.com/matteoferla/Epistasis_Calculator" target="_blank"><i class="fab fa-github"></i> Code repository</a>
                    </li>
                </ul>
            </div>
        </nav>
        <br>
        <div class="container">
            <div class="row">
                <div class="col-xl-10 offset-md-1">
                    ${ next.body() }
                </div>
            </div>
        </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"
        integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49"
        crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
<script src="https://d3js.org/d3.v5.min.js"></script>
<script src="https://cdn.rawgit.com/exupero/saveSvgAsPng/gh-pages/src/saveSvgAsPng.js"></script>
<%block name='code'/>

    </body>

</html>