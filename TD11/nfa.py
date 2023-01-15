from dg import *

# Question 5
def contains_pattern(s, text):
    sp = "(.)*" + s + "(.)*"
    nfa = NFA(sp)
    return nfa.check_text(text)

class NFA:
    def __init__(self, s): # s is the string containing the regular expression
        self.s = s
        self.m = len(self.s)
        self.dg = DG(len(s) + 1) # the directed graph that stores the epsilon links
        self.lp = [-1 for _ in range(len(s))]
        self.rp = [-1 for _ in range(len(s))]
        self.left_right_match_or() # assigns lp and rp according to parentheses matches
        self.build_eps_links() # assigns the epsilon links in self.dg

    def __str__(self):
        n = self.m
        str_lp = 'lp: '
        str_rp = 'rp: '
        for i in range(self.m):
            if self.lp[i] == -1:
                str_lp += '-1  '
            elif self.lp[i] < 10:
                str_lp += str(self.lp[i]) + '   '
            else: str_lp += str(self.lp[i]) + '  '
            if self.rp[i] == -1:
                str_rp += '-1  '
            elif self.rp[i] < 10:
                str_rp += str(self.rp[i]) + '   '
            else: str_rp += str(self.rp[i]) + '  '
        str_lp += '\n'
        str_rp += '\n'

        str_dg = str(self.dg)

        s = '------------------\nRegular expression\n------------------\n' + 're: ' + '   '.join(self.s) + '\n'
        return s + str_lp + str_rp #+ '------------------\nCorresponding NFA\n------------------\n' + str_dg

    ## Question 1
    def left_right_match(self):
        res = []
        for i in range(self.m):
            if self.s[i] == '(':
                res.append(i)
            elif self.s[i] == ')':
                j = res.pop()
                self.lp[i] = j
                self.rp[j] = i

    ## Question 2
    def left_right_match_or(self):
        res = []
        for i in range(self.m):
            if self.s[i] == '(' or self.s[i] == '|':
                res.append(i)
            elif self.s[i] == ')':
                j = res.pop()
                if self.s[j] == '|':
                    k = res.pop()
                    self.lp[i] = k
                    self.rp[k] = i
                    self.lp[j] = k
                    self.rp[j] = i
                else:
                    self.lp[i] = j
                    self.rp[j] = i

    ## Question 3
    def build_eps_links(self):
        for i in range(self.m):
            if self.s[i] in ['(', ')', '*']:
                self.dg.add_link(i,i+1)
        for i in range(self.m):
            rp = self.rp[i]
            lp = self.lp[i]
            if self.s[i] == '|':
                self.dg.add_link(lp, i + 1)
                self.dg.add_link(i, rp)
            if self.s[i] == '*':
                lp2 = self.lp[i - 1]
                self.dg.add_link(i, lp2)
                self.dg.add_link(lp2, i)

    ## Question 4
    # Complexity: O(mn)
    # Because: O(m) for the for loop, O(n) for the explore_from_subset method
    def check_text(self, w):
        '''
        We start with the case where w is the empty word. Let K be the set of states that can be reached from the initial
        state using a path of ε-links only. Clearly, the empty word is accepted if and only if the accepting state belongs
        to K. More generally, for a word w ofword w of length n, we let w(i) be the prefix of w of length i.
        For i from 0 to n, we maintain the set K(i) of states that are reachable from the initial state by
        consuming w(i). Note that we have already characterized K(0). For i ≥ 1, we let D(i) be the set
        of states that are obtained from a state in K(i−1) by following a black link that uses letter w[i − 1].
        Note that K(i) is then the set of states that are reachable from a state in D(i) by following a path of ε-links.

        returns True if the word w matches the regular expression self.s, and it returns False otherwise.
        To this end, make use of the method explore_from_subset(self, start_vertices) (of self.dg),
        which takes a list of indices of w and returns a list of indices of all states that are reachable via ε-links.
        '''
        links = self.dg.explore_from_subset([0])
        for i in range(len(w)):
            after = []
            for l in links:
                if l == self.m:
                    continue
                if self.s[l] == '.' or self.s[l] == w[i]:
                    after.append(l + 1)
            if (len(after)) == 0:
                return False
            links = self.dg.explore_from_subset(after)
        return self.m in links


