
// GET SEARCH FORM AND PAGE LINKS
let search_form = document.getElementById("search_form")
let page_links = document.getElementsByClassName("page--link")

// ENSURE SEACH FORM EXISTS

if(search_form){
    for(let i=0; page_links.length > i; i++){
        page_links[i].addEventListener("click",function (e){
            e.preventDefault()
            //GET DATA ATRIBUTE
            let page = this.dataset.page
                
            // ADD HIDDEN SEARCH INPUT TO FORM
            search_form.innerHTML += `<input value = ${page} name="page" hidden/> `
            // SUBMIT FORM
            search_form.submit()
        })
    }

}

