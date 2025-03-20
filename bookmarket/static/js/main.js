// 消息自动消失
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        $('.alert').alert('close');
    }, 3000);
});

// 确认删除对话框
function confirmDelete(event, message) {
    event.preventDefault();
    Swal.fire({
        title: '确认删除',
        text: message || "此操作不可撤销，确定要删除吗？",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消'
    }).then((result) => {
        if (result.isConfirmed) {
            event.target.form.submit();
        }
    });
}

// 图片预览
function previewImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#imagePreview').attr('src', e.target.result).show();
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// 书籍列表无限滚动加载
document.addEventListener('DOMContentLoaded', function() {
    let loading = false;
    const loadingElement = document.getElementById('loadingSpinner');
    const booksList = document.getElementById('booksList');
    
    // 如果不在书籍列表页面，直接返回
    if (!booksList) {
        return;
    }

    window.addEventListener('scroll', function() {
        if (loading) return;

        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
            loading = true;
            if (loadingElement) loadingElement.style.display = 'block';

            // 获取下一页数据
            const nextPage = parseInt(window.currentPage) + 1;
            
            fetch(`/books/load-more/?page=${nextPage}`)
                .then(response => response.json())
                .then(data => {
                    if (data.books && data.books.length > 0) {
                        data.books.forEach(book => {
                            const bookElement = `
                                <div class="col-md-4 mb-4">
                                    <div class="card">
                                        ${book.image ? `<img src="${book.image}" class="card-img-top" alt="${book.title}">` : ''}
                                        <div class="card-body">
                                            <h5 class="card-title">${book.title}</h5>
                                            <p class="card-text">
                                                作者: ${book.author}<br>
                                                价格: <span class="price-tag">¥${book.price}</span><br>
                                                成色: <span class="condition-tag condition-${book.condition}">${book.condition_display}</span>
                                            </p>
                                            <a href="/books/${book.id}/" class="btn btn-primary">查看详情</a>
                                        </div>
                                    </div>
                                </div>
                            `;
                            booksList.insertAdjacentHTML('beforeend', bookElement);
                        });
                        
                        window.currentPage = nextPage;
                    }
                    loading = false;
                    if (loadingElement) loadingElement.style.display = 'none';
                })
                .catch(error => {
                    console.error('Error loading more books:', error);
                    loading = false;
                    if (loadingElement) loadingElement.style.display = 'none';
                });
        }
    });
});

// 实时搜索
let searchTimeout;
$('.search-input').on('input', function(e) {
    e.preventDefault();  // 防止表单提交
    const resultsContainer = $('#searchResults');
    clearTimeout(searchTimeout);
    
    const query = $(this).val().trim();
    if (query.length < 2) {
        resultsContainer.addClass('d-none');
        return;
    }
    
    searchTimeout = setTimeout(function() {
        $.get('/books/search/', { q: query })
            .done(function(response) {
                if (response.results && response.results.length > 0) {
                    updateSearchResults(response.results);
                    resultsContainer.removeClass('d-none');
                } else {
                    resultsContainer.html('<div class="p-3">未找到相关书籍</div>');
                    resultsContainer.removeClass('d-none');
                }
            })
            .fail(function() {
                resultsContainer.addClass('d-none');
            });
    }, 300);
});

// 点击其他地方时隐藏搜索结果
$(document).on('click', function(e) {
    if (!$(e.target).closest('.search-form').length) {
        $('#searchResults').addClass('d-none');
    }
});

function updateSearchResults(results) {
    const resultsContainer = $('#searchResults');
    resultsContainer.empty();
    
    results.forEach(function(book) {
        resultsContainer.append(`
            <div class="search-result-item">
                <a href="/books/${book.id}/">
                    <img src="${book.image || '/static/images/no-image.png'}" alt="${book.title}">
                    <div class="search-result-info">
                        <h6>${book.title}</h6>
                        <p>¥${book.price}</p>
                    </div>
                </a>
            </div>
        `);
    });
} 