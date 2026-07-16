import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        # YOUR CODE HERE
        orders = self.data['orders'].copy()
        df = orders[orders['order_status'] == 'delivered']

        time_columns = [
            'order_purchase_timestamp',
            'order_approved_at',
            'order_delivered_carrier_date',
            'order_delivered_customer_date',
            'order_estimated_delivery_date'
        ]
        
        for col in time_columns:
            df[col] = pd.to_datetime(df[col])

        df['wait_time'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp'])/np.timedelta64(1, 'D')
        df['expected_wait_time'] = (df['order_estimated_delivery_date'] - df['order_purchase_timestamp'])/np.timedelta64(1, 'D')

        delay = df['expected_wait_time'] - df['wait_time']

        df['delay_vs_expected'] = np.where(delay > 0, delay, 0)
        
        return df[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        # YOUR CODE HERE
        df = self.data['order_reviews'].copy()
        
        df['dim_is_five_star'] = df['review_score'].map({5: 1}).fillna(0).astype(int)
        df['dim_is_one_star'] = df['review_score'].apply(lambda x: 1 if x == 1 else 0)

        return df[['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]

    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        # YOUR CODE HERE
        df = self.data['order_items'].copy()
        return df.groupby('order_id').count()\
            .rename(columns={"order_item_id": "number_of_items"})\
            .sort_values("number_of_items", ascending=False)[['number_of_items']]\
            .reset_index()[['order_id', 'number_of_items']]      

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        # YOUR CODE HERE
        df = self.data['order_items'].copy()
        return df.groupby('order_id').count()\
            .rename(columns={"seller_id": "number_of_sellers"})\
            .sort_values("number_of_sellers", ascending=False)[['number_of_sellers']]\
            .reset_index()[['order_id', 'number_of_sellers']] 

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        pass  # YOUR CODE HERE

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        pass  # YOUR CODE HERE
