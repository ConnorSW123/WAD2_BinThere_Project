import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2_BinThere_Project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from BinThere.models import Location, BinType, Bin, Vote

def populate():
    # First, create some users
    user1 = User.objects.get_or_create(username="user1")[0]
    user2 = User.objects.get_or_create(username="user2")[0]
    user3 = User.objects.get_or_create(username="user3")[0]

    print("Users populated!")

    # Now create some locations
    loc1 = Location.objects.get_or_create(name="University of Glasgow", latitude="55.8780", longitude="-4.2900")[0]
    loc2 = Location.objects.get_or_create(name="Kelvingrove Park", latitude="55.8701", longitude="-4.2855")[0]
    loc3 = Location.objects.get_or_create(name="Botanic Gardens", latitude="55.8764", longitude="-4.2952")[0]
    loc4 = Location.objects.get_or_create(name="Glasgow Cathedral", latitude="55.8602", longitude="-4.2473")[0]
    loc5 = Location.objects.get_or_create(name="The Hunterian", latitude="55.8713", longitude="-4.2902")[0]

    print("Locations populated!")

    # Now create some bin types
    pet_bin_type = BinType.objects.get_or_create(name="PET Bottle")[0]
    glass_bin_type = BinType.objects.get_or_create(name="Glass")[0]
    plastic_bin_type = BinType.objects.get_or_create(name="Soft Plastic")[0]
    paper_bin_type = BinType.objects.get_or_create(name="Paper")[0]
    metal_bin_type = BinType.objects.get_or_create(name="Metal")[0]

    print("Bin types populated!")

    # Now create some bins at these locations with initial upvotes and downvotes
    bin1 = Bin.objects.get_or_create(location=loc1, bin_type=pet_bin_type, added_by=user1, upvotes=5, downvotes=2)[0]
    bin2 = Bin.objects.get_or_create(location=loc2, bin_type=glass_bin_type, added_by=user2, upvotes=3, downvotes=1)[0]
    bin3 = Bin.objects.get_or_create(location=loc3, bin_type=plastic_bin_type, added_by=user3, upvotes=7, downvotes=0)[0]
    bin4 = Bin.objects.get_or_create(location=loc4, bin_type=paper_bin_type, added_by=user1, upvotes=0, downvotes=4)[0]
    bin5 = Bin.objects.get_or_create(location=loc5, bin_type=metal_bin_type, added_by=user2, upvotes=2, downvotes=3)[0]

    print("Bins populated!")

    # Now add some allocated votes to users for the bins
    votes_data = [
        {'bin': bin1, 'user': user1, 'vote': 1},  # Upvote for bin 1
        {'bin': bin2, 'user': user2, 'vote': -1}, # Downvote for bin 2
        {'bin': bin3, 'user': user1, 'vote': 1},  # Upvote for bin 3
        {'bin': bin4, 'user': user3, 'vote': -1}, # Downvote for bin 4
        {'bin': bin5, 'user': user2, 'vote': 1},  # Upvote for bin 5
    ]

    # Add each vote to the database
    for vote_data in votes_data:
        Vote.objects.get_or_create(bin=vote_data['bin'], user=vote_data['user'], vote=vote_data['vote'])

    print("Votes populated!")

# Start execution here
if __name__ == '__main__':
    print('Starting BinThere population script...')
    populate()
