var cards = $(".product-card")

data_arr = []
for (var i = 0; i < cards.length; i++) {

    const element = cards[i];
    const link = element.querySelector('.product-card__link').getAttribute('href');
    const revenue = element.querySelector('.product-card__revenue-number').textContent.trim();
    const revenue_period = element.querySelector('.product-card__revenue-period').textContent.trim();
    const revenue_explanation = element.querySelector('.product-card__revenue-explanation').textContent.trim();

    const data = {
        link,
        revenue,
        revenue_period,
        revenue_explanation,
    };
    data_arr.push(data);
}

////////////////////////////////////////////////////////////////////////

function scrollDownToEnd() {
    let scrollHeight = document.body.scrollHeight;
    let currentScroll = window.scrollY;

    if (currentScroll < scrollHeight) {
        window.scrollTo(0, currentScroll + 10);
        setTimeout(scrollDownToEnd, 10); // Adjust delay if needed
    }
}

scrollDownToEnd();


/////////////////////////////////////////////////////////////////////////


var cards = $(".product-card")

data_arr = []
for (var i = 0; i < cards.length; i++) {

    const element = cards[i];
    const linkElement = element.querySelector('.product-card__link');
    const revenueElement = element.querySelector('.product-card__revenue-number');
    const revenuePeriodElement = element.querySelector('.product-card__revenue-period');
    const revenueExplanationElement = element.querySelector('.product-card__revenue-explanation');

    const link = linkElement ? linkElement.getAttribute('href') : 'does not exist';
    const revenue = revenueElement ? revenueElement.textContent.trim() : 'does not exist';
    const revenue_period = revenuePeriodElement ? revenuePeriodElement.textContent.trim() : 'does not exist';
    const revenue_explanation = revenueExplanationElement ? revenueExplanationElement.textContent.trim() : 'does not exist';

    const data = {
        link,
        revenue,
        revenue_period,
        revenue_explanation,
    };
    data_arr.push(data);


}
