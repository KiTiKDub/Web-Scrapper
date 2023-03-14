document.addEventListener('DOMContentLoaded', function(e) {
    let index = 0;
    userId = document.querySelector('#userID').value
    

    //this allows for the colors to change on the thumbs, as well as prevent both of them being on
    document.querySelectorAll('.interact').forEach(function() { 
        
        let thumbs = document.querySelector(`#art-${index}`).getElementsByTagName('svg')
        let like = thumbs[0]
        let dislike = thumbs[1]


        like.addEventListener('click', () => {
            if(like.getAttribute('fill') === 'none') {
                like.setAttribute('fill', 'lightblue')

                idFinder = like.id.split('-').pop()

                fetch('/liked', {
                    method: "POST",
                    body: JSON.stringify({
                        article_id: idFinder,
                        user_liked_id: userId,
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message)
                    if(data.message === "You've already liked this Article!") {
                        D = document.createElement('div')
                        text = document.createTextNode("You've already liked this Article!")
                        D.appendChild(text)
                        like.replaceWith(D)
                    } 
 
                })

                if(dislike.getAttribute('fill') != 'none') {
                    dislike.setAttribute('fill', 'none')
                }
            }
        })

        dislike.addEventListener('click', () => {
            if(dislike.getAttribute('fill') === 'none') {
                dislike.setAttribute('fill', '#FFCCCB')

                idFinder = dislike.id.split('-').pop()

                fetch('/disliked', {
                    method: "POST",
                    body: JSON.stringify({
                        article_id: idFinder,
                        user_disliked_id: userId,
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if(data.message === "You've already disliked this Article!") {
                        D = document.createElement('div')
                        text = document.createTextNode("You've already disliked this Article!")
                        D.appendChild(text)
                        dislike.replaceWith(D)
                    } 
                })

                if(like.getAttribute('fill') != 'none') {
                    like.setAttribute('fill', 'none')
                }
            }
        })

        index = index + 1;
    })

     document.addEventListener('click', event => {
        let element = event.target

        // this is a fetch call to pull up the past search
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
            //this returns the table 
        } else if(element.tagName === 'DIV') { 
            document.querySelector('.table').style.removeProperty('display')
            document.querySelector('.table').style.width = '100%'
            document.querySelector('.found-articles').style.display = 'none'
        }
        
    }) 
    
    //this prints the fetch call
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