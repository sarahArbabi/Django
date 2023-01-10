from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.db.models import Q,Max,Min
from cart.models import *
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from .filters import ProductsFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    category = Category.objects.filter(sub_cat=False)
    products = Product.objects.all().order_by('-create')[:9]
    return render(request,'home/home.html',{'category':category,'products':products})



def all_products(request,id = None,slug=None):
    products = Product.objects.all()
    min = Product.objects.aggregate(unit_price=Min('unit_price'))
    min_price = int(min['unit_price'])
    max = Product.objects.aggregate(unit_price=Max('unit_price'))
    max_price = int(max['unit_price'])
    filter = ProductsFilter(request.GET,queryset=products)
    products = filter.qs
    paginator = Paginator(products,6)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    category = Category.objects.filter(sub_cat = False)
    search_form = Search()
    if id and slug:
        data = Category.objects.get(id=id, slug=slug)
        page_obj = Product.objects.filter(category=data)
    return render(request,'home/products.html',{'products':page_obj,'category':category,'filter':filter,'min_price':min_price,'max_price':max_price})


def details(request,id):
    product = get_object_or_404(Product,id=id)
    ip = request.META.get('REMOTE_ADDR')
    view = Views.objects.filter(product_id=product.id,ip=ip)
    if not view.exists():
        Views.objects.create(product_id=product.id,ip=ip)
        product.num_view +=1
        product.save()
    if request.user.is_authenticated:
        product.view.add(request.user)
    similar = product.tags.similar_objects()[:2]
    is_like= False
    if product.like.filter(id=request.user.id).exists():
        is_like = True
    is_dislike = False
    if product.like.filter(id=request.user.id).exists():
        is_dislike = True
    commentform = CommentForm()
    comment = Comment.objects.filter(is_reply=False,product_id=id)
    replyform = ReplyForm()
    images = Images.objects.filter(product_image_id=id)
    cartform = CartForm()
    is_favorite = False
    if product.favorite.filter(id=request.user.id).exists():
        is_favorite=True
    if product.status != 'None':
        if request.method =='POST':
            variant = Variant.objects.filter(product_variant_id=id).distinct('color_variant__name')
            var_id = request.POST.get('select')
            vars_id = request.POST.get('selects')
            if var_id:
                variants = Variant.objects.get(id=var_id)
            elif vars_id:
                variants = Variant.objects.get(id=vars_id)
            vars = Variant.objects.filter(product_variant_id=id, color_variant__name__exact=variants.color_variant.name)
        else:
            variant = Variant.objects.filter(product_variant_id=id).distinct('color_variant__name')
            variants = Variant.objects.get(id=variant[0].id)
            vars = Variant.objects.filter(product_variant_id=id, color_variant__name__exact=variants.color_variant.name)
        context={'vars': vars,'product':product,'variant':variant,'variants':variants,'similar':similar,'is_like':is_like,'is_dislike':is_dislike,'commentform':commentform,'comment':comment,'replyform':replyform,'images':images,'cartform':cartform,'is_favorite':is_favorite}
        return render(request,'home/detail.html',context)
    else:
        return render(request, 'home/detail.html', {'product': product,'similar':similar,'is_like':is_like,'is_dislike':is_dislike,'commentform':commentform,'comment':comment,'replyform':replyform,'images':images,'cartform':cartform,'is_favorite':is_favorite})


def product_like(request,id):
    url = request.META.get('HTTP_REFERER')
    product =get_object_or_404(Product,id=id)
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
    else:
        product.like.add(request.user)
    return redirect(url)



def product_dislike(request,id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    if product.dislike.filter(id=request.user.id).exists():
        product.dislike.remove(request.user)
    else:
        product.dislike.add(request.user)
    return redirect(url)



def product_comment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            data = commentform.cleaned_data
            Comment.objects.create(comment=data['comment'],rate=data['rate'],user_id=request.user.id,product_id=id)
            return redirect(url)
        else:
            return redirect(url)



def product_reply(request,id,comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        replyform = ReplyForm(request.POST)
        if replyform.is_valid():
            data = replyform.cleaned_data
            Comment.objects.create(comment=data('comment'),user_id=request.user.id,product_id=id,reply_id=comment_id,is_reply=True)
            return redirect(url)
        else:
            return redirect(url)



def product_search(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = Search(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data.isdigit():
                products = products.filter(Q(discount__exact=data)|Q(unit_price__exact=data))
            else:
                products = products.filter(Q(name__icontains=data))
            return render(request,'home/products.html',{'products':products,'form':form})


@login_required(login_url='accounts:login')
def favorite(request,id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    if product.favorite.filter(id=request.user.id).exists():
        product.favorite.remove(request.user.id)
    else:
        product.favorite.add(request.user.id)
    return redirect(url)



def contact(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
        body = subject + '\n' + email + '\n' + message
        form = EmailMessage(
            'contact-form',
            body,
            'test',
            ('sarrrah.262@gmail.com',),
        )
        form.send(fail_silently=False)
    return render(request,'home/contact.html')



def compare(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        item = get_object_or_404(Product,id=id)
        qs = Compare.objects.filter(user_id=request.user.id,product_id=id)
        if qs.exists():
            messages.success(request,'added')
        else:
            Compare.objects.create(user_id=request.user.id,product_id=item.id,session_key=None)
    else:
        item = get_object_or_404(Product,id=id)
        qs = Compare.objects.filter(user_id=None,product_id=item.id,session_key=request.session.session_key)
        if qs.exists():
            messages.success(request, 'added')
        else:
            if not request.session.session_key:
                request.session.create()
            Compare.objects.create(user_id=None,product_id=item.id,session_key=request.session.session_key)
    return redirect(url)


def show(request):
    if request.user.is_authenticated:
        data = Compare.objects.filter(user_id=request.user.id)
        return render(request,'home/compare.html',{'data':data})
    else:
        data = Compare.objects.filter(session_key__exact=request.session.session_key,user_id=None)
        return render(request, 'home/compare.html', {'data': data})


def product_view(request):
    view= Product.objects.filter(view=request.user.id)
    return render(request,'home/products.html',{'view':view})