from app.core.db import SessionLocal
from app.models.brand import Brand
from app.models.product import Product

from app.models import Product, Ingredient, Brand


db = SessionLocal()

# -------------------------------
# 🌍 International Brands
# -------------------------------

the_ordinary = Brand(
    name="The Ordinary",
    country="Canada",
    website_url="https://theordinary.com",
    image_url="https://brandfetch.com/theordinary.com?view=library&library=default&collection=logos&asset=idpxGYNMtA&utm_source=https%253A%252F%252Fbrandfetch.com%252Ftheordinary.com&utm_medium=copyAction&utm_campaign=brandPageReferral",
    is_international=True
)
cerave = Brand(
    name="CeraVe",
    country="USA",
    website_url="https://www.cerave.com",
    image_url = "https://brandfetch.com/cerave.com?view=library&library=default&collection=logos&asset=idRMvstMwe&utm_source=https%253A%252F%252Fbrandfetch.com%252Fcerave.com&utm_medium=copyAction&utm_campaign=brandPageReferral",
    is_international=True
)
beauty_of_joseon = Brand(
    name="Beauty of Joseon",
    country="South Korea",
    website_url="https://beautyofjoseon.com",
    image_url="https://brandfetch.com/beautyofjoseon.com?view=library&library=default&collection=logos&asset=idZLVB7rey&utm_source=https%253A%252F%252Fbrandfetch.com%252Fbeautyofjoseon.com&utm_medium=copyAction&utm_campaign=brandPageReferral",
    is_international=True
)
neutrogena = Brand(
    name="Neutrogena",
    country="USA",
    website_url="https://www.neutrogena.com",
    image_url="https://brandfetch.com/neutrogena.com?view=library&library=default&collection=logos&asset=idZVjE-xhE&utm_source=https%253A%252F%252Fbrandfetch.com%252Fneutrogena.com&utm_medium=copyAction&utm_campaign=brandPageReferral",
    is_international=True
)

# -------------------------------
# 🇵🇰 Pakistani Brands
# -------------------------------

petals = Brand(name="Petals Beauty", country="Pakistan", website_url="https://www.thepetalsbeauty.com", image_url="https://www.thepetalsbeauty.com/logo.png", is_international=False)
mcosmetics = Brand(name="M.Cosmetics", country="Pakistan", website_url="https://mcosmeticsline.com", image_url="https://mcosmeticsline.com/logo.png", is_international=False)
oneskin = Brand(name="OneSkin", country="Pakistan", website_url="https://oneskinofficial.com", image_url="https://oneskinofficial.com/logo.png", is_international=False)
saeed_ghani = Brand(name="Saeed Ghani", country="Pakistan", website_url="https://saeedghani.pk", image_url="https://saeedghani.pk/logo.png", is_international=False)
nirvana = Brand(name="Nirvana Botanics", country="Pakistan", website_url="https://nirvanabotanics.com", image_url="https://nirvanabotanics.com/logo.png", is_international=False)
her_beauty = Brand(name="Her Beauty", country="Pakistan", website_url="https://joinherbeauty.com", image_url="https://joinherbeauty.com/logo.png", is_international=False)
jenpharm = Brand(name="Jenpharm", country="Pakistan", website_url="https://jenpharm.com", image_url="https://jenpharm.com/logo.png", is_international=False)
otwo = Brand(name="O.Two.O", country="Pakistan", website_url="https://otwoo.com.pk", image_url="https://otwoo.com.pk/logo.png", is_international=False)
missrose = Brand(name="Miss Rose", country="Pakistan", website_url="https://missrose.com.pk", image_url="https://missrose.com.pk/logo.png", is_international=False)
amna = Brand(name="Beautify by Amna", country="Pakistan", website_url="https://bbabysuleman.com", image_url="https://bbabysuleman.com/logo.png", is_international=False)

# Add all brands
brands = [the_ordinary, cerave, beauty_of_joseon, neutrogena, petals, mcosmetics, oneskin, saeed_ghani, nirvana, her_beauty, jenpharm, otwo, missrose, amna]
db.add_all(brands)
db.commit()

# -------------------------------
# 🧴 Products
# -------------------------------

products =[
    # The Ordinary
    Product(name="Niacinamide 10% + Zinc 1%", category="Serum", price=10.80, product_url="https://theordinary.com/en-us/category/skincare/serums", image_url="https://theordinary.com/images/niacinamide.png", brand_id=the_ordinary.id),
    Product(name="Multi-Peptide + HA Serum", category="Serum", price=33.80, product_url="https://theordinary.com/en-us/multi-peptide-ha-serum-100613.html", image_url="https://theordinary.com/images/multi-peptide.png", brand_id=the_ordinary.id),
    Product(name="Glycolic Acid 7% Toning Solution", category="Toner", price=13.00, product_url="https://theordinary.com/products/glycolic-acid-toner", image_url="https://theordinary.com/images/glycolic-toner.png", brand_id=the_ordinary.id),
    Product(name="Squalane Cleanser", category="Cleanser", price=9.90, product_url="https://theordinary.com/products/squalane-cleanser", image_url="https://theordinary.com/images/squalane-cleanser.png", brand_id=the_ordinary.id),

    # CeraVe
    Product(name="Hydrating Cleanser", category="Cleanser", price=14.99, product_url="https://www.cerave.com/skincare/cleansers/hydrating-cleanser", image_url="https://www.cerave.com/images/hydrating-cleanser.png", brand_id=cerave.id),
    Product(name="Moisturizing Cream", category="Moisturizer", price=16.99, product_url="https://www.cerave.com/skincare/moisturizers/moisturizing-cream", image_url="https://www.cerave.com/images/moisturizing-cream.png", brand_id=cerave.id),
    Product(name="Foaming Facial Cleanser", category="Cleanser", price=13.99, product_url="https://www.cerave.com/products/foaming-cleanser", image_url="https://www.cerave.com/images/foaming-cleanser.png", brand_id=cerave.id),
    Product(name="AM Facial Moisturizing Lotion SPF 30", category="Moisturizer", price=18.99, product_url="https://www.cerave.com/products/am-lotion", image_url="https://www.cerave.com/images/am-lotion.png", brand_id=cerave.id),

    # Beauty of Joseon
    Product(name="Relief Sun SPF50+", category="Sunscreen", price=18.00, product_url="https://beautyofjoseon.com/products/relief-sun", image_url="https://beautyofjoseon.com/images/relief-sun.png", brand_id=beauty_of_joseon.id),
    Product(name="Glow Serum", category="Serum", price=17.00, product_url="https://beautyofjoseon.com/products/glow-serum", image_url="https://beautyofjoseon.com/images/glow-serum.png", brand_id=beauty_of_joseon.id),
    Product(name="Dynasty Cream", category="Moisturizer", price=22.00, product_url="https://beautyofjoseon.com/products/dynasty-cream", image_url="https://beautyofjoseon.com/images/dynasty-cream.png", brand_id=beauty_of_joseon.id),
    Product(name="Radiance Cleansing Balm", category="Cleanser", price=20.00, product_url="https://beautyofjoseon.com/products/cleansing-balm", image_url="https://beautyofjoseon.com/images/cleansing-balm.png", brand_id=beauty_of_joseon.id),

    # Neutrogena
    Product(name="Hydro Boost Gel Cream", category="Moisturizer", price=19.99, product_url="https://www.neutrogena.com/products/skincare/hydro-boost-gel-cream", image_url="https://www.neutrogena.com/images/hydro-boost.png", brand_id=neutrogena.id),
    Product(name="Oil-Free Acne Wash", category="Cleanser", price=8.99, product_url="https://www.neutrogena.com/products/oil-free-acne-wash", image_url="https://www.neutrogena.com/images/acne-wash.png", brand_id=neutrogena.id),
    Product(name="Ultra Sheer Dry-Touch Sunscreen SPF 55", category="Sunscreen", price=9.99, product_url="https://www.neutrogena.com/products/sunscreen", image_url="https://www.neutrogena.com/images/sunscreen.png", brand_id=neutrogena.id),
    Product(name="Makeup Remover Cleansing Towelettes", category="Cleanser", price=6.99, product_url="https://www.neutrogena.com/products/makeup-remover", image_url="https://www.neutrogena.com/images/makeup-remover.png", brand_id=neutrogena.id),
    # OneSkin
    Product(name="Hydrating Face Wash", category="Cleanser", price=1200, product_url="https://oneskinofficial.com/products/hydrating-face-wash", image_url="https://oneskinofficial.com/images/hydrating-face-wash.png", brand_id=oneskin.id),
    Product(name="Brightening Serum", category="Serum", price=1500, product_url="https://oneskinofficial.com/products/brightening-serum", image_url="https://oneskinofficial.com/images/brightening-serum.png", brand_id=oneskin.id),
    Product(name="Soothing Gel", category="Skincare", price=1000, product_url="https://oneskinofficial.com/products/soothing-gel", image_url="https://oneskinofficial.com/images/soothing-gel.png", brand_id=oneskin.id),
    Product(name="Nourishing Night Cream", category="Moisturizer", price= 1800, product_url="https://oneskinofficial.com/products/nourishing-night-cream", image_url="https://oneskinofficial.com/images/nourishing-night-cream.png", brand_id=oneskin.id),
    # Petals Beauty
    Product(name="Matte Lipstick", category="Makeup", price=850, product_url="https://www.thepetalsbeauty.com/products/matte-lipstick", image_url="https://www.thepetalsbeauty.com/images/matte-lipstick.png", brand_id=petals.id),
    Product(name="Glow Highlighter", category="Makeup", price=1200, product_url="https://www.thepetalsbeauty.com/products/glow-highlighter", image_url="https://www.thepetalsbeauty.com/images/glow-highlighter.png", brand_id=petals.id),
    Product(name="BB Cream", category="Makeup", price=950, product_url="https://www.thepetalsbeauty.com/products/bb-cream", image_url="https://www.thepetalsbeauty.com/images/bb-cream.png", brand_id=petals.id),
    Product(name="Blush Palette", category="Makeup", price=1350, product_url="https://www.thepetalsbeauty.com/products/blush-palette", image_url="https://www.thepetalsbeauty.com/images/blush-palette.png", brand_id=petals.id),

    # M.Cosmetics
    Product(name="Blush Stain", category="Makeup", price=1100, product_url="https://mcosmeticsline.com/products/blush-stain", image_url="https://mcosmeticsline.com/images/blush-stain.png", brand_id=mcosmetics.id),
    Product(name="Hydrating Serum", category="Skincare", price=1500, product_url="https://mcosmeticsline.com/products/hydrating-serum", image_url="https://mcosmeticsline.com/images/hydrating-serum.png", brand_id=mcosmetics.id),
    Product(name="Lip Tint", category="Makeup", price=750, product_url="https://mcosmeticsline.com/products/lip-tint", image_url="https://mcosmeticsline.com/images/lip-tint.png", brand_id=mcosmetics.id),
    Product(name="Glow Mist", category="Skincare", price=1300, product_url="https://mcosmeticsline.com/products/glow-mist", image_url="https://mcosmeticsline.com/images/glow-mist.png", brand_id=mcosmetics.id),

    # Her Beauty
    Product(name="Clean Toner", category="Skincare", price=1400, product_url="https://joinherbeauty.com/products/clean-toner", image_url="https://joinherbeauty.com/images/clean-toner.png", brand_id=her_beauty.id),
    Product(name="Hydrating Gel", category="Skincare", price=1600, product_url="https://joinherbeauty.com/products/hydrating-gel", image_url="https://joinherbeauty.com/images/hydrating-gel.png", brand_id=her_beauty.id),
    Product(name="SPF Moisturizer", category="Skincare", price=1800, product_url="https://joinherbeauty.com/products/spf-moisturizer", image_url="https://joinherbeauty.com/images/spf-moisturizer.png", brand_id=her_beauty.id),
    Product(name="Night Cream", category="Skincare", price=2000, product_url="https://joinherbeauty.com/products/night-cream", image_url="https://joinherbeauty.com/images/night-cream.png", brand_id=her_beauty.id),

    # Jenpharm
    Product(name="AcneX Face Wash", category="Cleanser", price=950, product_url="https://jenpharm.com/products/acnex-face-wash", image_url="https://jenpharm.com/images/acnex-face-wash.png", brand_id=jenpharm.id),
    Product(name="HydraFix Moisturizer", category="Moisturizer", price=1150, product_url="https://jenpharm.com/products/hydrafix", image_url="https://jenpharm.com/images/hydrafix.png", brand_id=jenpharm.id),
    Product(name="SunBlock SPF60", category="Sunscreen", price=1350, product_url="https://jenpharm.com/products/sunblock", image_url="https://jenpharm.com/images/sunblock.png", brand_id=jenpharm.id),
    Product(name="Glow Serum", category="Serum", price=1450, product_url="https://jenpharm.com/products/glow-serum", image_url="https://jenpharm.com/images/glow-serum.png", brand_id=jenpharm.id),

    # O.Two.O
    Product(name="Velvet Lipstick", category="Makeup", price=650, product_url="https://otwoo.com.pk/products/velvet-lipstick", image_url="https://otwoo.com.pk/images/velvet-lipstick.png", brand_id=otwo.id),
    Product(name="Liquid Foundation", category="Makeup", price=950, product_url="https://otwoo.com.pk/products/liquid-foundation", image_url="https://otwoo.com.pk/images/liquid-foundation.png", brand_id=otwo.id),
    Product(name="Blush Compact", category="Makeup", price=850, product_url="https://otwoo.com.pk/products/blush-compact", image_url="https://otwoo.com.pk/images/blush-compact.png", brand_id=otwo.id),
    Product(name="Contour Stick", category="Makeup", price=900, product_url="https://otwoo.com.pk/products/contour-stick", image_url="https://otwoo.com.pk/images/contour-stick.png", brand_id=otwo.id),

    # Miss Rose
    Product(name="Matte Lip Gloss", category="Makeup", price=550, product_url="https://missrose.com.pk/products/matte-lip-gloss", image_url="https://missrose.com.pk/images/matte-lip-gloss.png", brand_id=missrose.id),
    Product(name="Eyeshadow Palette", category="Makeup", price=1250, product_url="https://missrose.com.pk/products/eyeshadow-palette", image_url="https://missrose.com.pk/images/eyeshadow-palette.png", brand_id=missrose.id),
    Product(name="Liquid Eyeliner", category="Makeup", price=450, product_url="https://missrose.com.pk/products/liquid-eyeliner", image_url="https://missrose.com.pk/images/liquid-eyeliner.png", brand_id=missrose.id),
    Product(name="Compact Powder", category="Makeup", price=700, product_url="https://missrose.com.pk/products/compact-powder", image_url="https://missrose.com.pk/images/compact-powder.png", brand_id=missrose.id),
    # Beautify by Amna
    Product(name="Hydrating Face Mist", category="Skincare", price=1200, product_url="https://bbabysuleman.com/products/hydrating-face-mist", image_url="https://bbabysuleman.com/images/hydrating-face-mist.png", brand_id=amna.id),
    Product(name="Brightening Serum", category="Serum", price=1500, product_url="https://bbabysuleman.com/products/brightening-serum", image_url="https://bbabysuleman.com/images/brightening-serum.png", brand_id=amna.id),
    Product(name="Soothing Gel", category="Skincare", price=1000, product_url="https://bbabysuleman.com/products/soothing-gel", image_url="https://bbabysuleman.com/images/soothing-gel.png", brand_id=amna.id),
    Product(name="Nourishing Night Cream", category="Moisturizer", price= 1800, product_url="https://bbabysuleman.com/products/nourishing-night-cream", image_url="https://bbabysuleman.com/images/nourishing-night-cream.png", brand_id=amna.id)
]
niacinamide = Ingredient(
    name="Niacinamide",
    inci_name="Niacinamide",
    category="Active",
    function="Brightening",
    description="Improves skin tone and texture.",
    benefits=["Reduces inflammation", "Minimizes pores"],
    side_effects=["Mild irritation"],
    comedogenic_rating=1,
    is_natural=True,
    safety_score=9.5
)

glycerin = Ingredient(
    name="Glycerin",
    inci_name="Glycerin",
    category="Humectant",
    function="Hydration",
    description="Draws moisture into the skin.",
    benefits=["Hydrates skin", "Improves barrier function"],
    side_effects=[],
    comedogenic_rating=0,
    is_natural=True,
    safety_score=10.0
)

glow_serum = Product(
    name="Glow Serum",
    category="Serum",
    price=1500,
    product_url="https://oneskinofficial.com/products/brightening-serum",
    ingredients=[niacinamide, glycerin]
)

products.append(glow_serum)
db.add_all([niacinamide, glycerin])
db.add_all(products)
db.commit()
db.close()



    

