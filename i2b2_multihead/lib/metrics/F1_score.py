from typing import Dict, List, Tuple, Set, Optional
from abc import ABC, abstractmethod
from overrides import overrides


class F1_abc(object):
    def __init__(self):
        self.A = 1e-10
        self.B = 1e-10
        self.C = 1e-10
        self.A0 = 1e-10
        self.B0 = 1e-10
        self.C0 = 1e-10
        self.A1 = 1e-10
        self.B1 = 1e-10
        self.C1 = 1e-10
        self.A2 = 1e-10
        self.B2 = 1e-10
        self.C3 = 1e-10
        self.A4 = 1e-10
        self.B4 = 1e-10
        self.C4 = 1e-10
        self.A5 = 1e-10
        self.B5 = 1e-10
        self.C5 = 1e-10
        self.A6 = 1e-10
        self.B6 = 1e-10
        self.C6 = 1e-10
        self.A7 = 1e-10
        self.B7 = 1e-10
        self.C7 = 1e-10

    def reset(self) -> None:
        self.A = 1e-10
        self.B = 1e-10
        self.C = 1e-10
        self.A0 = 1e-10
        self.B0 = 1e-10
        self.C0 = 1e-10
        self.A1 = 1e-10
        self.B1 = 1e-10
        self.C1 = 1e-10
        self.A2 = 1e-10
        self.B2 = 1e-10
        self.C2 = 1e-10
        self.A3 = 1e-10
        self.B3 = 1e-10
        self.C3 = 1e-10
        self.A4 = 1e-10
        self.B4 = 1e-10
        self.C4 = 1e-10
        self.A5 = 1e-10
        self.B5 = 1e-10
        self.C5 = 1e-10
        self.A6 = 1e-10
        self.B6 = 1e-10
        self.C6 = 1e-10
        self.A7 = 1e-10
        self.B7 = 1e-10
        self.C7 = 1e-10
    def get_metric(self, reset: bool = False):
        if reset:
            self.reset()

        f1, p, r = 2 * self.A / (self.B +
                                  self.C), self.A / self.B, self.A / self.C
        result = {"precision": p, "recall": r, "fscore": f1}

        return result
    def get_metric0(self, count , reset: bool = False):
        if reset:
            self.reset()
        if count == 0:
            a = self.A0
            b = self.B0
            c = self.C0
        elif count == 1:
            a = self.A1
            b = self.B1
            c = self.C1
        elif count == 2:
            a = self.A2
            b = self.B2
            c = self.C2
        elif count == 3:
            a = self.A3
            b = self.B3
            c = self.C3
        elif count == 4:
            a = self.A4
            b = self.B4
            c = self.C4
        elif count == 5:
            a = self.A5
            b = self.B5
            c = self.C5
        elif count == 6:
            a = self.A6
            b = self.B6
            c = self.C6
        elif count == 7:
            a = self.A7
            b = self.B7
            c = self.C7
        f1, p, r = 2 * a / (b +
                                 c), a / b, a / c
        result = {"precision": p, "recall": r, "fscore": f1}

        return result

    # def get_metric1(self, reset: bool = False):
    #     if reset:
    #         self.reset()
    #
    #     f1, p, r = 2 * self.A1 / (self.B1 +
    #                              self.C1), self.A1 / self.B1, self.A1 / self.C1
    #     result = {"precision": p, "recall": r, "fscore": f1}
    #
    #     return result
    #
    # def get_metric2(self, reset: bool = False):
    #     if reset:
    #         self.reset()
    #
    #     f1, p, r = 2 * self.A2 / (self.B2 +
    #                              self.C2), self.A2 / self.B2, self.A2 / self.C2
    #     result = {"precision": p, "recall": r, "fscore": f1}
    #
    #     return result
    # def get_metric3(self, reset: bool = False):
    #     if reset:
    #         self.reset()
    #
    #     f1, p, r = 2 * self.A3 / (self.B3 +
    #                              self.C3), self.A3 / self.B3, self.A3 / self.C3
    #     result = {"precision": p, "recall": r, "fscore": f1}
    #
    #     return result
    # def get_metric4(self, reset: bool = False):
    #     if reset:
    #         self.reset()
    #
    #     f1, p, r = 2 * self.A4 / (self.B4 +
    #                              self.C4), self.A4 / self.B4, self.A4 / self.C4
    #     result = {"precision": p, "recall": r, "fscore": f1}
    #
    #     return result
    #
    # def get_metric5(self, reset: bool = False):
    #     if reset:
    #         self.reset()
    #
    #     f1, p, r = 2 * self.A5 / (self.B5 +
    #                              self.C5), self.A5 / self.B5, self.A5 / self.C5
    #     result = {"precision": p, "recall": r, "fscore": f1}
    #
    #     return result
    #
    # def get_metric6(self, reset: bool = False):
    #     if reset:
    #         self.reset()
    #
    #     f1, p, r = 2 * self.A6 / (self.B6 +
    #                              self.C6), self.A6 / self.B6, self.A6 / self.C6
    #     result = {"precision": p, "recall": r, "fscore": f1}
    #
    #     return result
    #
    # def get_metric7(self, reset: bool = False):
    #     if reset:
    #         self.reset()
    #
    #     f1, p, r = 2 * self.A7 / (self.B7 +
    #                              self.C7), self.A7 / self.B7, self.A7 / self.C7
    #     result = {"precision": p, "recall": r, "fscore": f1}
    def __call__(self, predictions,
                 gold_labels):
        raise NotImplementedError


class F1_triplet(F1_abc):

    @overrides
    def __call__(self, predictions: List[List[Dict[str, str]]],
                 gold_labels: List[List[Dict[str, str]]]):

        for g, p in zip(gold_labels, predictions):
            try:
                g_set = set('_'.join((gg['object'], gg['predicate'],
                                    gg['subject'])) for gg in g)
                p_set = set('_'.join((pp['object'], pp['predicate'],
                                    pp['subject'])) for pp in p)
            except:
                g_set = set('_'.join((''.join(gg['object']), gg['predicate'],
                                    ''.join(gg['subject']))) for gg in g)
                p_set = set('_'.join((''.join(pp['object']), pp['predicate'],
                                    ''.join(pp['subject']))) for pp in p)
                # 为什么这里要用try和except
            self.A += len(g_set & p_set)
            self.B += len(p_set)
            self.C += len(g_set)


            try:
                g0_set = set('_'.join((gg['object'], gg['predicate'],
                                      gg['subject'])) for gg in g if gg['predicate'] == 'TrAP')
                p0_set = set('_'.join((pp['object'], pp['predicate'],
                                      pp['subject'])) for pp in p if pp['predicate'] == 'TrAP')
            except:
                g0_set = set('_'.join((''.join(gg['object']), gg['predicate'],
                                      ''.join(gg['subject']))) for gg in g if gg['predicate'] == 'TrAP')
                p0_set = set('_'.join((''.join(pp['object']), pp['predicate'],
                                      ''.join(pp['subject']))) for pp in p if pp['predicate'] == 'TrAP')
            self.A0 += len(g0_set & p0_set)
            self.B0 += len(p0_set)
            self.C0 += len(g0_set)

            try:
                g1_set = set('_'.join((gg['object'], gg['predicate'],
                                       gg['subject'])) for gg in g if gg['predicate'] == 'TrCP')
                p1_set = set('_'.join((pp['object'], pp['predicate'],
                                       pp['subject'])) for pp in p if pp['predicate'] == 'TrCP')
            except:
                g1_set = set('_'.join((''.join(gg['object']), gg['predicate'],
                                       ''.join(gg['subject']))) for gg in g if gg['predicate'] == 'TrCP')
                p1_set = set('_'.join((''.join(pp['object']), pp['predicate'],
                                       ''.join(pp['subject']))) for pp in p if pp['predicate'] == 'TrCP')
            self.A1 += len(g1_set & p1_set)
            self.B1 += len(p1_set)
            self.C1 += len(g1_set)

            try:
                g2_set = set('_'.join((gg['object'], gg['predicate'],
                                       gg['subject'])) for gg in g if gg['predicate'] == 'TeCP')
                p2_set = set('_'.join((pp['object'], pp['predicate'],
                                       pp['subject'])) for pp in p if pp['predicate'] == 'TeCP')
            except:
                g2_set = set('_'.join((''.join(gg['object']), gg['predicate'],
                                       ''.join(gg['subject']))) for gg in g if gg['predicate'] == 'TeCP')
                p2_set = set('_'.join((''.join(pp['object']), pp['predicate'],
                                       ''.join(pp['subject']))) for pp in p if pp['predicate'] == 'TeCP')
            self.A2 += len(g2_set & p2_set)
            self.B2 += len(p2_set)
            self.C2 += len(g2_set)

            try:
                g3_set = set('_'.join((gg['object'], gg['predicate'],
                                       gg['subject'])) for gg in g if gg['predicate'] == 'PIP')
                p3_set = set('_'.join((pp['object'], pp['predicate'],
                                       pp['subject'])) for pp in p if pp['predicate'] == 'PIP')
            except:
                g3_set = set('_'.join((''.join(gg['object']), gg['predicate'],
                                       ''.join(gg['subject']))) for gg in g if gg['predicate'] == 'PIP')
                p3_set = set('_'.join((''.join(pp['object']), pp['predicate'],
                                       ''.join(pp['subject']))) for pp in p if pp['predicate'] == 'PIP')
            self.A3 += len(g3_set & p3_set)
            self.B3 += len(p3_set)
            self.C3 += len(g3_set)

            try:
                g4_set = set('_'.join((gg['object'], gg['predicate'],
                                       gg['subject'])) for gg in g if gg['predicate'] == 'TrNAP')
                p4_set = set('_'.join((pp['object'], pp['predicate'],
                                       pp['subject'])) for pp in p if pp['predicate'] == 'TrNAP')
            except:
                g4_set = set('_'.join((''.join(gg['object']), gg['predicate'],
                                       ''.join(gg['subject']))) for gg in g if gg['predicate'] == 'TrNAP')
                p4_set = set('_'.join((''.join(pp['object']), pp['predicate'],
                                       ''.join(pp['subject']))) for pp in p if pp['predicate'] == 'TrNAP')
            self.A4 += len(g4_set & p4_set)
            self.B4 += len(p4_set)
            self.C4 += len(g4_set)

            try:
                g5_set = set('_'.join((gg['object'], gg['predicate'],
                                       gg['subject'])) for gg in g if gg['predicate'] == 'TrIP')
                p5_set = set('_'.join((pp['object'], pp['predicate'],
                                       pp['subject'])) for pp in p if pp['predicate'] == 'TrIP')
            except:
                g5_set = set('_'.join((''.join(gg['object']), gg['predicate'],
                                       ''.join(gg['subject']))) for gg in g if gg['predicate'] == 'TrIP')
                p5_set = set('_'.join((''.join(pp['object']), pp['predicate'],
                                       ''.join(pp['subject']))) for pp in p if pp['predicate'] == 'TrIP')
            self.A5 += len(g5_set & p5_set)
            self.B5 += len(p5_set)
            self.C5 += len(g5_set)

            try:
                g6_set = set('_'.join((gg['object'], gg['predicate'],
                                       gg['subject'])) for gg in g if gg['predicate'] == 'TrWP')
                p6_set = set('_'.join((pp['object'], pp['predicate'],
                                       pp['subject'])) for pp in p if pp['predicate'] == 'TrWP')
            except:
                g6_set = set('_'.join((''.join(gg['object']), gg['predicate'],
                                       ''.join(gg['subject']))) for gg in g if gg['predicate'] == 'TrWP')
                p6_set = set('_'.join((''.join(pp['object']), pp['predicate'],
                                       ''.join(pp['subject']))) for pp in p if pp['predicate'] == 'TrWP')
            self.A6 += len(g6_set & p6_set)
            self.B6 += len(p6_set)
            self.C6 += len(g6_set)

            try:
                g7_set = set('_'.join((gg['object'], gg['predicate'],
                                       gg['subject'])) for gg in g if gg['predicate'] == 'TeRP')
                p7_set = set('_'.join((pp['object'], pp['predicate'],
                                       pp['subject'])) for pp in p if pp['predicate'] == 'TeRP')
            except:
                g7_set = set('_'.join((''.join(gg['object']), gg['predicate'],
                                       ''.join(gg['subject']))) for gg in g if gg['predicate'] == 'TeRP')
                p7_set = set('_'.join((''.join(pp['object']), pp['predicate'],
                                       ''.join(pp['subject']))) for pp in p if pp['predicate'] == 'TeRP')
            self.A7 += len(g7_set & p7_set)
            self.B7 += len(p7_set)
            self.C7 += len(g7_set)
class F1_ner(F1_abc):

    @overrides
    def __call__(self, predictions: List[List[str]], gold_labels: List[List[str]]):
        for g, p in zip(gold_labels, predictions):

            # inter = sum(tok_g == tok_p and tok_g in ('B', 'I')
            #             for tok_g, tok_p in zip(g, p))
            # bi_g = sum(tok_g in ('B', 'I') for tok_g in g)
            # bi_p = sum(tok_p in ('B', 'I') for tok_p in p)
            inter = sum(tok_g == tok_p and tok_g[0] in ('B', 'I')
                        for tok_g, tok_p in zip(g, p))
            bi_g = sum(tok_g[0] in ('B', 'I') for tok_g in g)
            bi_p = sum(tok_p[0] in ('B', 'I') for tok_p in p)
            self.A += inter
            self.B += bi_g
            self.C += bi_p
