from app.core.db import SessionLocal
from app.models.user import User
from app.models.brand import Brand
from app.models.product import Product
from app.models.ingredient import Ingredient

db = SessionLocal()

# -------------------------------
# 👤 Create a default user for seeding
# -------------------------------
seed_user = User(
    email="admin@example.com",
    password="admin123",   # ⚠️ plaintext for seed, hash later
    hashed_password="admin123",
    full_name="Seed Admin"
)
db.add(seed_user)
db.commit()
db.refresh(seed_user)

# -------------------------------
# 🌍 International Brands
# -------------------------------
the_ordinary = Brand(
    name="The Ordinary",
    country="Canada",
    website="https://theordinary.com",
    is_international=True,
    user_id=seed_user.id
)
cerave = Brand(
    name="CeraVe",
    country="USA",
    website="https://www.cerave.com",
    is_international=True,
    user_id=seed_user.id
)
beauty_of_joseon = Brand(
    name="Beauty of Joseon",
    country="South Korea",
    website="https://beautyofjoseon.com",
    is_international=True,
    user_id=seed_user.id
)
neutrogena = Brand(
    name="Neutrogena",
    country="USA",
    website="https://www.neutrogena.com",
    is_international=True,
    user_id=seed_user.id
)

# 🇵🇰 Pakistani Brands
petals = Brand(name="Petals Beauty", country="Pakistan", website="https://www.thepetalsbeauty.com", user_id=seed_user.id)
mcosmetics = Brand(name="M.Cosmetics", country="Pakistan", website="https://mcosmeticsline.com", user_id=seed_user.id)
oneskin = Brand(name="OneSkin", country="Pakistan", website="https://oneskinofficial.com", user_id=seed_user.id)
saeed_ghani = Brand(name="Saeed Ghani", country="Pakistan", website="https://saeedghani.pk", user_id=seed_user.id)
nirvana = Brand(name="Nirvana Botanics", country="Pakistan", website="https://nirvanabotanics.com", user_id=seed_user.id)
her_beauty = Brand(name="Her Beauty", country="Pakistan", website="https://joinherbeauty.com", user_id=seed_user.id)
jenpharm = Brand(name="Jenpharm", country="Pakistan", website="https://jenpharm.com", user_id=seed_user.id)
otwo = Brand(name="O.Two.O", country="Pakistan", website="https://otwoo.com.pk", user_id=seed_user.id)
missrose = Brand(name="Miss Rose", country="Pakistan", website="https://missrose.com.pk", user_id=seed_user.id)
amna = Brand(name="Beautify by Amna", country="Pakistan", website="https://bbabysuleman.com", user_id=seed_user.id)

brands = [
    the_ordinary, cerave, beauty_of_joseon, neutrogena,
    petals, mcosmetics, oneskin, saeed_ghani,
    nirvana, her_beauty, jenpharm, otwo, missrose, amna
]

db.add_all(brands)
db.commit()

# -------------------------------
# 🧴 Products (simplified example)
# -------------------------------
products = [
    Product(name="Niacinamide 10% + Zinc 1%", category="Serum", price=10.80, brand_id=the_ordinary.id, user_id=seed_user.id),
    Product(name="Hydrating Cleanser", category="Cleanser", price=14.99, brand_id=cerave.id, user_id=seed_user.id),
]

# -------------------------------
# 🌿 Ingredients
# -------------------------------
niacinamide = Ingredient(
    name="Niacinamide",
    inci_name="Niacinamide",
    category="Active",
    function="Brightening",
    description="Improves skin tone and texture.",
    benefits="Reduces inflammation, Minimizes pores",
    side_effects="Mild irritation",
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
    benefits="Hydrates skin, Improves barrier function",
    side_effects="",
    comedogenic_rating=0,
    is_natural=True,
    safety_score=10.0
)

db.add_all([niacinamide, glycerin])
db.add_all(products)
db.commit()
db.close()

print("✅ Database seeded successfully with brands, products, and ingredients!")
