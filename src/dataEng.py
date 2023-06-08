import pandas as pd

class FeatureEngineering:
    """
    A feature engineering class.
    Contains methods to engineer new
    features from existing ones.


    Attributes
    ----------
    data : pd.DataFrame
        The data which will be engineered
    

    Methods
    -------
    engineer_features() -> pd.DataFrame
        Engineer new features for self.data from existing ones

    is_date(c : pd.Series) -> bool
        Checks whether the row c contains a valid date

    is_this_year(c : pd.Series) -> bool
        Checks whether the row c contains the same year that the draw happend

    is_post_2000(c : pd.Series) -> bool
        Checks whether the row c contains the a valid year past the year 2000

    get_lucky_numbers(c : pd.Series) -> int
        Checks how many lucky numbers the row c contains

    get_all_7_numbers(sc : pd.Series) -> int
        Checks how many numbers the row c contains that all have the number 7
    """

    def __init__(self, df : pd.DataFrame) -> None:
        self.data = df

    def is_date(self, c : pd.Series) -> bool:
        """ 
        Checks whether the row c contains
        a valid date. E.g.
        5. 10.  -- > True
        if no such dates are found, it returns false

        Parameters
        ----------
        c : pandas.Series
            the rows that will be checked

        Returns
        -------
        bool
            the truth value of whether the row 
            contains a valid date
        """

        day = False
        month = False
        for lab, i in c.iteritems():
            if 'N' not in lab: continue

            if not month:
                if i <= 12: month = True
            elif not day:
                if i <= 31: day = True
            else:
                break
        return day and month

    def is_this_year(self, c : pd.Series) -> bool:
        """ 
        Checks whether the row c contains
        the same year that the draw happend

        Parameters
        ----------
        c : pandas.Series
            the rows that will be checked
        
        Returns
        -------
        bool
            the truth value of whether the row 
            contains the current year
        """
        first = 20
        second = c['YYYY']-2000

        f, s = False, False
        for lab, i in c.iteritems():
            if 'N' not in lab: continue

            if   i == first:  f = True
            elif i == second: s = True
        
        return f and s

    def is_post_2000(self, c : pd.Series) -> bool:
        """ 
        Checks whether the row c contains
        the a valid year past the year 2000

        Parameters
        ----------
        c : pandas.Series
            the rows that will be checked
        
        Returns
        -------
        bool
            the truth value of whether the row 
            contains a year after 2000
        """
        first = 20
        second = c['YYYY']-2000

        f, s = False, False
        for lab, i in c.iteritems():
            if 'N' not in lab: continue

            if   i == 20:  f = True
            elif i <= second: s = True
        
        return f and s

    def get_lucky_numbers(self, c : pd.Series) -> int:
        """ 
        Checks how many lucky numbers the row c contains

        Parameters
        ----------
        c : pandas.Series
            the rows that will be checked
        
        Returns
        -------
        int
            The number of lucky numbers in the data
        """

        # these lucky numbers are directly from the web 
        # https://schoolworkhelper.net/numerology-lucky-unlucky-numbers/
        # Supposedlty some people really believe in these numbers
        lucky_numbers = [1, 3, 7, 9, 13, 15, 21, 25, 31, 33, 37, 43, 49] 
        total = 0
        for n in lucky_numbers:
            total += n in c.values
        return total

    def get_all_7_numbers(self, c : pd.Series) -> int:
        """ 
        Checks how many numbers the row c contains
        that all have the number 7
        7, 17, 27, 37, 47

        Parameters
        ----------
        c : pandas.Series
            the rows that will be checked
        
        Returns
        -------.is_post_2000,
        int
            The number of numbers in the data matching the pattern
        """

        # Supposedly some people actually bet on
        # number 7 so much that they want a combination 
        # with all 7s...
        # Ref:
        # https://uk.movies.yahoo.com/most-popular-lottery-numbers-040000570.html
        pattern = [7, 17, 27, 37, 47] 
        total = 0
        for n in pattern:
            total += n in c.values
        return total
    
    def engineer_features(self) -> pd.DataFrame:
        """
        Engineer new features for self.data from existing ones.
        Note that these new features are completely hard-coded.

        Returns
        -------
        pd.DataFrame
            The newly engineered features
        """

        N_numbers = self.data.loc[:,'YYYY':'N5']
        L_numbers = self.data.loc[:, ['L1', 'L2']]

        # ---------------------------- date-based-features -----------------------------------------
        self.data["is date"]      = N_numbers.apply(self.is_date, axis = 1)
        self.data["is post 2000"] = N_numbers.apply(self.is_post_2000, axis = 1)
        self.data["is this year"] = N_numbers.apply(self.is_this_year, axis = 1)
        # ---------------------------- lucky-numbers-based features -----------------------------------------
        self.data["lucky numbers"]      = N_numbers.apply(self.get_lucky_numbers, axis = 1)
        self.data["lucky lucky numbers"]= L_numbers.apply(self.get_lucky_numbers, axis = 1)
        self.data["has lucky"]          = self.data["lucky numbers"]>0
        self.data["has lucky lucky"]    = self.data["lucky lucky numbers"]>0
        # ---------------------------- unlucky-numbers-based features -----------------------------------------
        self.data["7 pattern"]          = N_numbers.apply(self.get_all_7_numbers, axis = 1)
        # ---------------------------- betting-no-based features -----------------------------------------
        self.data["N sum"]     = N_numbers.loc[:,'N1':].apply(lambda c: c.sum(), axis = 1)
        self.data["L sum"]     = L_numbers.apply(lambda c: c.sum(), axis = 1)
        self.data["N sum big"] = self.data["N sum"] > self.data["N sum"].mean()
        self.data["L sum big"] = self.data["L sum"] > self.data["L sum"].mean()

        #  ---------------------------- binning features -----------------------------------------
        from sklearn.preprocessing import LabelEncoder
        label_encoder = LabelEncoder()
        self.data['N sum bin']   = label_encoder.fit_transform(pd.cut(self.data['N sum'], 6))
        self.data['L sum bin']   = label_encoder.fit_transform(pd.cut(self.data['L sum'], 6))
        self.data['NL sum']      = self.data['N sum'] + self.data['L sum']
        self.data['NL sum bin']  = label_encoder.fit_transform(pd.cut(self.data["NL sum"], 6))

        # ---------------------------- drop unwanted values -----------------------------------------
        for col in ['Day', 'DD', 'MMM', 'YYYY', 'Wins']:
            if col in self.data.columns:
                self.data.drop(columns = [col], inplace=True)

        return self.data