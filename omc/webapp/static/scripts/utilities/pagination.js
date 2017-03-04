var Paginatior = function(paginatorClass, pages, changeFunction, initPage, reload = true) {
    var paginator = $(paginatorClass);
    var page = typeof initPage !== 'undefined' ? initPage : 1;
    var pageSelector = paginator.find('.page-selector');

    var pages = pages > 1 ? pages : 1;

    page = page > pages ? pages : page;

    pageSelector.empty();
    for (i = 1; i <= pages; ++i) {
        pageSelector.append('<option value="' + i + '">' + i + '</option>');
    }

    var setPage = function(page) {
        if (page <= 1) {
            paginator.find('.btn-go-first-page').addClass('disabled');
            paginator.find('.btn-go-previous-page').addClass('disabled');
        } else {
            paginator.find('.btn-go-first-page').removeClass('disabled');
            paginator.find('.btn-go-previous-page').removeClass('disabled');
        }
        if (page >= pages) {
            paginator.find('.btn-go-next-page').addClass('disabled');
            paginator.find('.btn-go-last-page').addClass('disabled');
        } else {
            paginator.find('.btn-go-next-page').removeClass('disabled');
            paginator.find('.btn-go-last-page').removeClass('disabled');
        }
    }

    paginator.find('.btn-go-first-page').click(function() {
        page = 1;
        changePage();
    });

    paginator.find('.btn-go-previous-page').click(function() {
        if (page > 1) {
            --page;
            changePage();
        }
    });

    paginator.find('.btn-go-next-page').click(function() {
        if (page < pages) {
            ++page;
            changePage();
        }
    });

    paginator.find('.btn-go-last-page').click(function() {
        page = pages;
        changePage();
    });

    var changePage = function(reload = true) {
        if (reload) {
            changeFunction(page);
        }
        paginator.find('.page-selector').val(page);
        setPage(page);
    }

    paginator.find('.page-selector').change(function() {
        page = $(this).val();
        changePage();
    });

    changePage(reload);
};
