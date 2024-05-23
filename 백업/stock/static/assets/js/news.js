document.getElementById('newsForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let company = document.getElementById('company').value;
    let maxpage = document.getElementById('maxpage').value;
    getCompanyCode(company, maxpage);
});

async function getCompanyCode(company, maxpage) {
    try {
        let response = await fetch('companylist.txt');
        let text = await response.text();
        let lines = text.split('\n');
        let dict = {};

        lines.forEach(line => {
            let [name, code] = line.split('\t');
            dict[name.trim()] = code.trim();
        });

        let pattern = /[a-zA-Z가-힣]+/;
        if (pattern.test(company)) {
            let companyCode = dict[company];
            if (companyCode) {
                await crawler(companyCode, maxpage);
            } else {
                alert('회사 이름을 찾을 수 없습니다.');
            }
        } else {
            await crawler(company, maxpage);
        }
    } catch (error) {
        console.error('Error fetching company codes:', error);
    }
}

async function crawler(companyCode, maxpage) {
    let newsContainer = document.getElementById('newsContainer');
    newsContainer.innerHTML = ''; // Clear previous news
    let page = 1;
    let newsHtml = '';

    while (page <= parseInt(maxpage)) {
        try {
            let url = `https://cors-anywhere.herokuapp.com/https://finance.naver.com/item/news_news.nhn?code=${companyCode}&page=${page}`;
            let response = await fetch(url);
            let text = await response.text();
            let parser = new DOMParser();
            let html = parser.parseFromString(text, 'text/html');

            let titles = html.querySelectorAll('.title');
            let dates = html.querySelectorAll('.date');
            let sources = html.querySelectorAll('.info');

            titles.forEach((title, index) => {
                let titleText = title.innerText.trim();
                let link = 'https://finance.naver.com' + title.querySelector('a').getAttribute('href');
                let date = dates[index].innerText.trim();
                let source = sources[index].innerText.trim();

                newsHtml += `<p><a href="${link}" target="_blank">${titleText}</a> - ${date} - ${source}</p>`;
            });

            page++;
        } catch (error) {
            console.error('Error fetching news:', error);
            break;
        }
    }

    newsContainer.innerHTML = newsHtml;
}
