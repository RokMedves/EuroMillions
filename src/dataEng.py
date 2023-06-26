import pandas as pd
from scipy.special import binom
import itertools
class FeatureEngineering:
    """
    A feature engineering class.
    Contains methods to engineer new
    features from existing ones.


    Attributes
    ----------
    data : pd.DataFrame
        The data which will be engineered
    
    win_frac: dict
        The fraction of the prize pool for each winning category (See ../datasets/README.md for details)

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

    number_of_different_rows(r : pd.Series) -> int
        Return how many different rows on the EuroMillions ticket needed to be marked to get the betting number in row r.

    drop_unwanted_values() -> pd.DataFrame
        Drop unwanted information from the dataframe    
    
    prob_NL_analyt(N: int, L : int) -> float
        Computes the probability to get N normal and L lucky numbers right in a draw

    score_numbers(row: pd.Series) -> float
        Given a row from the euromillions dataset, generate a score for the given number with the recipe described in euromillions.ipynb

    score_dataset(df : pd.DataFrame) -> pd.DataFrame
        Scores the datset by assigning an 'avg win' column representing the average winnings relative to the whole dataset
    
    """

    def __init__(self, df : pd.DataFrame) -> None:
        self.data = df

        self.win_frac= {5: {0: 0.0061, 1: 0.0261, 2: 0.5000},
                        4: {0: 0.0026, 1: 0.0035, 2: 0.0019},
                        3: {0: 0.0270, 1: 0.0145, 2: 0.0037},
                        2: {0: 0.1659, 1: 0.1030, 2: 0.0130},
                        1: {2: 0.0327}}


    #
    # --------------------------------- Methods for new features ---------------------------------
    #
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
        -------
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
    
    def number_of_different_rows(self, r : pd.Series) -> int:
        """
        Return how many different rows on the EuroMillions ticket 
        needed to be marked to get the betting number in row r.

        That is, imagine needing to physically bet on the number
        on a betting ticket. If all the numbers were drawn from the
        same row, return 1, if 2 different rows, then 2, and so on

        Parameters
        ----------
        r : pandas.Series
            the rows that will be checked
        
        Returns
        -------
        int
            The number of different rows in the ticket needed for the number
        """ 

        # the rows on the Euromillions ticket (see https://www.euromillions.eu.com/imagenes/euromillions-ticket.jpg)
        bins=[0, 8, 16, 24, 32, 40, 48, 50]
        # mask for selecting only N1 -> N5
        Nmask = ['N'+str(i+1) for i in range(5)]
        binned_row = pd.cut(r[Nmask], bins=bins)
        return len(binned_row.unique())


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
        self.data["N rows"]    = N_numbers.apply(self.number_of_different_rows, axis=1)
        self.data["N sum"]     = N_numbers.loc[:,'N1':].apply(lambda c: c.sum(), axis = 1)
        self.data["L sum"]     = L_numbers.apply(lambda c: c.sum(), axis = 1)
        self.data["N sum big"] = self.data["N sum"] > self.data["N sum"].mean()
        self.data["L sum big"] = self.data["L sum"] > self.data["L sum"].mean()

        #  ---------------------------- binning features -----------------------------------------
        from sklearn.preprocessing import LabelEncoder
        label_encoder = LabelEncoder()
        self.data['N sum bin']   = label_encoder.fit_transform(pd.cut(self.data['N sum'], 10))
        self.data['L sum bin']   = label_encoder.fit_transform(pd.cut(self.data['L sum'], 6))
        self.data['NL sum']      = self.data['N sum'] + self.data['L sum']
        self.data['NL sum bin']  = label_encoder.fit_transform(pd.cut(self.data["NL sum"], 6))

    
    def drop_unwanted_values(self) -> pd.DataFrame:
        """
        Drop unwanted information from the dataframe

        Returns
        -------
        pd.DataFrame
            The dataframe without the unused columns
        """

        # ---------------------------- drop unwanted values -----------------------------------------
        # Written in a slightly awkward way to nesure that different
        # bits of code can use these functions regardless of whether
        # the underlying classes have these columns
        for col in ['Day', 'DD', 'MMM', 'YYYY', 'Wins']:
            if col in self.data.columns:
                self.data.drop(columns = [col], inplace=True)

        return self.data
    

    #
    # --------------------------------- Methods for creating target variable ---------------------------------
    #

    def prob_NL_analyt(self, N: int, L : int, Lmax = 12) -> float:
        """ Computes the probability to get N normal and L lucky numbers right in a draw

        Parameters
        ----------
        N : int
            Number of correct drawn normal numbers
        L : int
            Number of correct drawn lucky number
        Lmax : int
            The number of lucky numbers in the draw pool. 12 today
        Returns
        -------
            Probability Pr[win in category N+L]
        """
        return binom(5, N) * binom(45, 5-N) * binom(2, L) * binom(Lmax-2, 2-L) / (binom(50, 5) * binom(Lmax, 2))

    # do this row per row
    def score_numbers(self, row: pd.Series) -> float:
        """
        Given a row from the euromillions dataset, generate 
        a score for the given number with the recipe described in euromillions.ipynb.
        If called with pd.apply(), this function generates a
        whole pd.Series().

        Parameters
        ----------
        row: pd.Series
            Row of the data to score

        Returns
        -------
            average winnigs for that number
        """

        # The scoring must be date-specific. 
        # As mentioned in ./datasets/README.md, the number of drawn lucky numers changed:
        # -> After  Sep 24th 2016, the maximum number of lucky numbers was 12
        # -> Before Sep 24th 2016 and after May 10th 2011, the maximum number was 11
        #
        # The below code therefore differentiates between the two cases

        # Figure out what Lmax we need to use depending on the date in the row 
        # Logic: Lmax = 12 if
        # 1) it's after 2016 OR 
        # 2) if it's the year 2016, but it's after September OR
        # 3) it's september 2016, but after the 24th
        if  (row['YYYY'] > 2016) or \
            (row['YYYY'] == 2016) * (row['MMM'] in ['Oct', 'Nov', 'Dec']) or\
            (row['YYYY'] == 2016) * (row['MMM'] == 'Sep') * (row['DD'] >= 24):
            Lmax = 12
        else:
            Lmax = 11

        avg_win = 0
        # loop through the possible winning groups
        for N, L in itertools.product(range(1, 6), range(0, 3)):
            nl_tag = str(N)+ ("+"+str(L) if L!=0 else "")
            if nl_tag in row.index:
                pr_nl_win   = self.prob_NL_analyt(N, L, Lmax) # Pr[N,L] = Pr[N,L | win] * 1/13 from above
                nl_win_frac = self.win_frac[N][L]       # f_p,k=(N,L)
                num_winners = row[nl_tag]
                num_sales   = row['Sales']

                f_w_nl      = (0 if num_winners == 0 else num_sales/num_winners) # f_w,k=(N,L)

                avg_win += pr_nl_win * nl_win_frac * f_w_nl
                # Diagnostic print 
                # print("k = {0}\t\tPr[N,L] = {1:.4f}, f_w,k = {2:.4f}, n_k = {3}\t\tE[win] = {4}".format(nl_tag, pr_nl_win, nl_win_frac, num_winners, avg_win))
        return avg_win

    def score_dataset(self, df : pd.DataFrame) -> pd.DataFrame:
        """
        Scores the datset by assigning an 'avg win' column
        representing the average winnings relative to the
        whole dataset

        Parameters
        ----------
        df: pd.DataFrame
            The DataFrame to be scored 
        Returns
        -------
        pd.DataFrame
            The scored dataframe
        """
        # generate the average winnings for each number
        scores = df.apply(self.score_numbers, axis = 'columns')
        # devide by the mean of each, thus getting the final score
        scores = scores / scores.mean()

        # incorporate that into the euromillions dataset
        df = pd.concat([df, scores], axis = 1).rename(columns={0: 'avg win'})


        return df
