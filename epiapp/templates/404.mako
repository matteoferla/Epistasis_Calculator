<%inherit file="layout.mako"/>
<div class="card p-2">
    <h3 class="card-header bg-dark">
        <a class="collapsed card-link text-light" data-toggle="collapse" href="#res"><i class="far fa-angle-down"></i>Error ${request.response.status_code}</a>
    </h3>
    <div class="card-body collapse show" id="res">
        <p>${request.response.status}</p>
    </div>
</div>
