document.addEventListener('DOMContentLoaded', function(e) {
    let index = 0;

    document.querySelectorAll('.interact').forEach(function() {
        
        let thumbs = document.querySelector(`#art-${index}`).getElementsByTagName('svg')
        let like = thumbs[0]
        let dislike = thumbs[1]


        like.addEventListener('click', e => {
            if(like.style.fill === 'none') {
                like.style.fill = 'lightblue'

                if(dislike.style.fill != 'none') {
                    dislike.style.fill = 'none'
                }
            }
            else {
                like.style.fill = 'none'
            }
        })

        dislike.addEventListener('click', () => {
            if(dislike.style.fill === 'none') {
                dislike.style.fill = '#FFCCCB'

                if(like.style.fill != 'none') {
                    like.style.fill = 'none'
                }
            }
            else {
                dislike.style.fill = 'none'
            }
        })

        index = index + 1;
    })

    document.addEventListener('click', event => {
        let element = event.target

        if(element.tagName === 'TD') {
            fetch(`history/${element.className}`)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                document.querySelector('.table').style.display = 'none'
                clear = document.createElement('div')
                clear.className = 'clear'
                clear.innerHTML = 'Click here to return to table'
                document.querySelector('.found-articles').append(clear)
                data.forEach(print)
            })
        } else if(element.tagName === 'DIV') {
            document.querySelector('.clear').addEventListener('click', () => {
                document.querySelector('.table').style.removeProperty('display')
                document.querySelector('.table').style.width = '100%'
                document.querySelector('.found-articles').style.display = 'none'
            })
        }
        
    })
    

    function print(context) {
        new_div = document.querySelector('.found-articles')
        new_div.style.display = 'block'
        new_div.style.paddingTop = '5rem'

        headline = document.createElement('h2')
        headline.className = 'headline'
        headline.innerHTML = context.headline
        headline.style.borderTop = 'solid'
        headline.style.paddingTop = '1rem'
        new_div.append(headline)

        body = document.createElement('div')
        body.className = 'article-body'
        body.innerHTML = context.body
        new_div.append(body)

        url = document.createElement('div')
        url.className = 'article-body'
        new_div.append(url)
        anchor = document.createElement('a')
        anchor.href = context.url
        anchor.innerHTML = 'Read full article'
        url.append(anchor)
    }
})