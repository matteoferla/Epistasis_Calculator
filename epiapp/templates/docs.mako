<%inherit file="layout.mako"/>
<!---Intro-->
<div class="card p-2">
    <h3 class="card-header bg-dark">


        <a class="card-link text-light" data-toggle="collapse" href="#calc"><i class="far fa-angle-down"></i>&#xA0;&#xA0;&#xA0;Calculations</a>


    </h3>
    <div class="card-body" id="calc">
        <p>Steps involved:</p>
        <ul>
            <li>The data is subtracted by the mean of the wild type. </li>
            <li>The sum of these zero-centered replicates plus the mean of the wild type is the theoretical mean assuming that these values are additive (i.e. have no epistasis).</li>
            <li>The theoretical standard error is calculated by taking the square root of the sum the variances of the sets of replicates divided by number of replicates.</li>
            <li>If the epistatic effect is beneficial, it is positive (+), if detrimental negative (-). Depending on the contributing values, there are different types of epistasis.</li>

            <li>When the beneficial or detrimental gains of the base mutations simply stack by summation, (ie. without epistasis), this is <b>additive</b>.</li>
            <li>When base mutations with the beneficial and detrimental gains are combined, but the result is greater than simply additive, this us <b>sign epistasis</b>.</li>
            <li>When the beneficial or detrimental gains of the base mutations stack more than expected, this is <b>magnitude epistasis</b>.</li>
            <li>When the beneficial or detrimental gains of the base mutations result in the reverse effect, this is <b>reciprocal sign epistasis</b>.</li>
        </ul>
    </div>
</div>


<%block name="code">
    <script>
        $(document).ready(function () {
            $('#calc').collapse('show');
        });
    </script>
</%block>