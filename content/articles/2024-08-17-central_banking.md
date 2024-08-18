---
Title: Central (Non-Free) Banking
Date: 2024-08-17 07:00:00 +0200
Tags: econ
slug: central_banking
---

From the previous article on [free banking](https://aceofgreens.github.io/free_banking.html), we saw how a competitive market for loans and deposits will result in virtually no inflation and a fixed money supply. In this post we'll enter the belly of the beast and see how central banking is designed to eliminate the constaints that keep inflation in check. This is a very important topic for understanding financial systems and once again, almighty Rothbard will guide us.

We start with a contrived, but concrete scenario. Person P deposits \$1000 in currency (physical money like coins and banknotes) in bank A. He receives a piece of paper called a "certificate of deposit" worth \$1000 which is liquid enough and is accepted by society *as money*. While this is supposed to be a proper demand deposit, bank A then decides to lend \$800 of these. It does so by printing another certificate of deposit worth \$800 and "giving it" to a new person Q by creating an account for Q in its own books. At this point the total demand deposits are worth \$1800 but the actual reserves are only \$1000. The money supply has increased by \$800. Now person Q spends the money and buys something from person R. If R is a client of the same bank A, then the balance of account Q has to be reduced and the balance of account R has to be increased. This happens easily since bank A simply rewrites the certificates of deposit. But if R is a client of a different bank B, then B, being a competitor of A, will demand from A money in specie and A will have to pay from its reserves. Suppose it does so and its reserves end up \$200. At this point, if the original person P decides to withdraw his deposit, bank A will become insolvent and will go bankrupt.

Thus, as long as we have competing banks with clients partitioned between them, some inflationary loans will lead to bankruptcies, which is a limiting factor on the increase of the money supply. On the other hand, if there is a single bank and everyone is a client of it, this bank can sustain the generation of inflationary loans out of thin air. The central bank is precisely this bank which, by force of the government, has all commercial banks as its clients.

A central bank (CB) can be considered an institution with the following properties:

- It and only it, is allowed to issue new bank notes or cash. All other privately-owned commercial banks are only allowed to issue demand liabilities in the form of checking deposits.
- Even when the banking system remains on the gold standard, virtually all bank holdings of gold are centralized into the central bank. This a classic requirement.

Consider what happens when a client of a commercial bank wants to cash in his deposit. The commercial bank is not permitted to issue these banknotes, only the central bank can. Therefore, the commercial bank needs to obtain Central Bank cash either by selling various assets to the CB that it agrees to buy, or by drawing down its own checking account with the central bank.

Thus, it becomes necessary for the commercial banks to have accounts in the central bank. A two-layered system develops. The first layer is between clients and commercial banks, think of it like a complicated bipartite graph. The second layer is between all the commercial banks and the single central bank. This is the *bottleneck* in the system which gives the central bank an immense power to affect the economy. How is this bottleneck enforced? Through government legislation and the force to punish those banks which do not adhere to the rules set.

Let's take a look at how these dynamics work. Suppose the fractional reserve ratio is 20%. Bank A has \$1000 worth of reserves at the CB and has pyramided \$5000 worth of warehouse certificates on top. It owns no gold and we are ignoring the CB notes kept for daily transactions which are in Bank A's vault, as they are only a small fraction.

|  | Bank A  |
|----:|----:|
|   **Assets** | **Liabilities**  |
| IOUs = \$4000     |  Demand deposits = \$5000  |
| Reserves = demand deposits at CB = \$1000  |   |

One of the bank's clients decides to withdraw \$500 from its account. But bank A has cannot issue any notes, so it goes to the CB and withdraws \$500 from its own account there. The CB issues these notes. After this transaction the balance sheet of bank A looks as follows. Note that only the form of the money has changed, not the actual money supply level.

|  | Bank A  |
|----:|----:|
|   **Assets** | **Liabilities**  |
| IOUs - \$4000     |  Demand deposits = \$4500  |
| Reserves = demand deposits at CB = \$500  |   |

But now the reserve ratio of bank A becomes 500/4500 = 1/9, below the requirement of 1/5. Bank A then needs to reduce its demand deposits from \$4500 to \$2500, so that the reserve ratio is again 1/5. It does so by failing to renew its loans, by rediscounting its IOUs to other financial institutions, and by selling its bonds and other assets on the market. The final balance sheet is as follows.

|  | Bank A  |
|----:|----:|
|   **Assets** | **Liabilities**  |
| IOUs = \$2000     |  Demand deposits = \$2500  |
| Reserves = demand deposits at CB = \$500  |   |

The money supply has been reduced by \$2000. Thus, under central banking, an increased demand for cash and the subsequent issue of new cash by the CB leads to a decrease in reserves and a decrease in the money supply, because of the banks' need to maintain their reserve ratios. In contrast, the deposit of cash by the public will have the opposite inflationary effect: as cash is deposited in a bank, its reserve ratio goes up above the minimum requirements. Since banks make money by lending, the bank will then increase the amount of loans it gives out and, by implication, its demand deposits. This will increase the money supply. The cash received by the bank from the initial deposit is deposited into its account at the CB. The CB takes the cash and retires/burns it.

The total money supply only includes money held by the public (demand deposits + CB notes). It does not include intrabank holdings like the CB demand deposits, as that would be double counting. Overall, the money supply is given by:

$$
M = \text{gold in public} + \text{CB notes in public} + \text{demand deposits of commercial banks}.
$$

If a country is taken off the gold standard, money becomes simply 
$$M = \text{CB notes in public} + \text{demand deposits of commercial banks}.$$

The inflationary potential of the CB depends on the public's desire to hold cash. The higher the demand for cash, the higher the limit on fractional reserve bank expansion. Similarly, if the demand for checking accounts increases, and thus the demand for cash decreases, so will the pressure for inflationary lending increase. Note that under a gold standard the CB *can* go bankrupt if the public insists on cashing in their deposits and CB paper for gold. To avoid this, most governments have conferred another important privilege to the CB - making its notes legal tender for all debts in money. Then, if A has contracted with B for a debt of \$1000 in money, B *has* to accept payment in CB notes; he cannot insist, for example, on gold.

The CB not only takes deposits, it also gives out loans. Thus, if a commercial bank cannot meet its liquidity needs, the CB can lend to it, or can agree to buy some of the bank's assets, in exchange for proper reserves. And this is a big difference compared to free banking. Here, if the CB is a *lender of last resort*, creating money out of thin air, it can save banks at will. What kind of incentives do you think this creates for private banks, which seemingly cannot, or are not allowed to fail?

As discussed so far, the inflation rate depends on the total reserves that banks hold above the minimum required ratio. In turn, these reserves depend on a few important factors:

1. **Demand for cash**. Suppose the public demands more cash from the commercial banks. They go to the CB and draw down their own reserves. The CB prints more notes and gives them to the commercial banks, which give them to the public. At this stage, total money supply has not changed, but the proportion of cash has increased at the expense of demand deposits. But then, to keep the same reserve ratio, banks have to decrease their total demand deposits. The end effect is that, if the public withdraws $x$ worth of deposits, reserves drop by $x$, and demand deposits drop by $x/r$, where $r$ is the minimum reserve ratio. Likewise, if the public deposits $x$, reserves go up by $x$, and demand deposits go up by $x/r$. 
2. **Demand for gold**. An increase in the public's demand for gold has a similar effect as an increase in demand for cash. The only difference is that when drawing down its deposits, the public asks for gold. The banks go to the CB and buy the gold by drawing down their own reserves at the CB. They then contract their demand deposits and the money supply shrinks.
3. **Loans to the banks**. The CB can provide temporary short-term (say a week) loans to commercial banks in need of immediate liquidity. Naturally this affects reserves. The interest rate charged by the Fed on its loans is called the *discount rate*. A higher discount rate makes borrowing from the Fed more expensive. Note that in the US, a bank in need of funds doesn't have to borrow from the Fed, it can borrow from other commercial banks which have reserves above the requirement. In fact, there is a big market for such reserves, called the *federal funds market*.
4. **Open Market Operations**. By far the most important determinant of total reserves, open market operations refer to the Fed directly buying or selling assets within different markets. Suppose person P is selling some asset to the Fed. The Fed then writes a check on itself (it creates its own liability) out of thin air, and hands over the check to person P. He has no other choice but to hand it over to his bank, which in turn rushes to hand it to the Fed in order to increase its reserves. With increased reserves, it can pyramid more loans on top of this check. There is no limit in terms of what the Fed buys or how much...

Now, we turn to the bank expansion process, specifically how it is that a bank can pyramid new demand deposits on top of an increase in reserves. Suppose $r=0.2$ and person P deposits \$1000 in bank A. Clearly, bank A's reserves go up by \$1000 and its demand deposits can go up by \$5000. But bank A cannot simply lend out a loan worth \$5000 because if the loan receiver spends this and gives it to a non-client of bank A, their bank will demand that \$5000 and bank A will go broke because it doesn't have it. Therefore, it lends only a fraction of it, $1-r$, or \$800. Here's precisely what happens:

1. Person P deposits \$1000 in bank A. Its reserves and demand deposits go up by \$1000.
2. Bank A lends out \$800 to person Q, increasing its demand deposits by a further \$800.
3. Person Q deposits \$800 in bank B. Bank B demands payment from bank A.
4. Bank A transfers \$800 from its reserves. B's reserves and demand deposits go up by \$800.
5. Bank A remains with increased reserves of \$200 and increased demand deposits of \$1000. It satisfies reserve requirements and is essentially out of the picture now.
6. Bank B is now in the same situation in which A was initially.

Bank B then lends out \$640, which reaches bank C. It lends out \$512 and so on. Total demand deposits across all banks go up by $1000 + 800 + 640 + 512 + ... = 5000$, as expected. All in all, if initial reserves go up by $x$, in the aggregate, demand deposits go by $x/r$ where $1/r$ is the *money multiplier*.

Consider a particularly nasty example of money creation to finance new government debt, a process called *debt monetization*. Suppose the government wants to run a \$100B deficit and needs the money to finance it. So it issues new bonds and sells them to the banks. This increases their demand deposits and hence the money supply by \$100B. Not only is this wildly inflationary, but the taxpayers will also be forced to pay back the \$100B over the years, plus a hefty amount of interest.

If banks are all loaned up, how did they get enough reserves to enable them to create the \$100B? In reality the process is as follows: the Fed buys \$25B of *old* bonds on the open market, increasing reserves and demand deposits by \$25B. Then, the Treasury issues \$100B of new bonds. Then the banks buy these new bonds. Total demand deposits are up by \$125B.

Another monstrous example. What happens if the Fed directly buys *newly created* government debt? The Treasury receives \$100B and spends it on its projects. The recipients of this money deposit it into their banks increasing total reserves by \$100B. Banks then pyramid on top, up to \$500B. *Is it not clear that the chronic and accelerating inflation of our time is caused by a fundamental change in the monetary system, precisely this introduction of central banking?*


Finally, it is an interesting question of how a central bank can develop in the first place. The following is a simplified historical narrative for how the Bank of England (BoE) came about.

1. In the late 17-th century, the British government needs money to fund a policy of war and imperialism against the French. Its credit rating is low and levying higher taxes is politically unfeasible. A new way of financing needs to be invented.
2. [William Paterson](https://en.wikipedia.org/wiki/William_Paterson_(banker)) comes up with a scheme where a new bank, the BoE, will issue new notes to buy new government bonds, as long as the government grants these notes the status of legal tender. The British government refuses, but allows the BoE to issue notes.
3. The BoE issues a huge sum, leading to inflation, and in two years, after a bank run, it becomes insolvent. This is caused by private goldsmiths want redemption in specie.
4. In May 1696 the government allows the BoE to *suspend specie payment* indefinitely. Its notes prompty fall to a 20% discount against specie. It resumes specie payments two years later, but in the future there are additional similar suspensions.
5. In 1696 the Tories almost succeed in creating a competing National Land Bank. To hinder competition, Parliament passes a law prohibiting any new corporate bank from being established in England. Counterfeiting of BoE notes is made punishable by death.
6. In 1708 another piece of legislation asserts *roughly* that corporations or institutions with more than six partners cannot issue notes redeemable on demand or make short-term loans under six months. Thus, the BoE starts enjoying the privilege of being the only bank (except very small institutions) that can issue bank notes.
7. In 1720, a formidable rival, the [South Sea Company](https://en.wikipedia.org/wiki/South_Sea_Company), collapses after a bout of inflationary monetary expansion. BoE also suffers a bank run.
8. In 1745 there is another bank run, due to the rising of [Bonnie Prince Charlie](https://en.wikipedia.org/wiki/Charles_Edward_Stuart) in Scotland. Both in 1720 and now, BoE is allowed to suspend species payment.
9. During the late 18th century, many small, private partnership banks start to hold BoE notes as reserves. Due to inflationary financing of the wars with France, in the period 1790-1797 many banks, including the BoE suspend specie payment. This suspension lasts 24 years.
10. During that time BoE notes serve as de facto legal tender. In 1812 they're made actual legal tender. When specie payments finally resume, BoE stocks fall substantially.
11. In 1833 banking is liberalized a bit, allowing banks within London to issue demand deposits. Country banks can now redeem in BoE notes.
12. From 1727 to 1850 Scotland enjoys a free banking system. Bank notes circulate freely but are not legal tender. Banks grow large and confidence in them soars. Each bank maintains its own specie reserves and is responsible for its solvency.
13. In 1844, Sir Robert Peel, a classical liberal, implements a fundamental banking reform with the intention of ending fractional reserve banking. Its provisions effectively eliminate country banks as issuers of bank notes, placing the monopoly of note issuing in the hands of the BoE, while at the same time forcing any new note issue by the BoE to be 100% backed by gold or silver. The plan was to have a only the BoE to issue notes, and to hold it to a 100% reserve requirement.
14. However, they overlooked that a monopoly-privileged bank protected by the state cannot be held to a restrictive 100% rule (as in general such power will be used and abused), and that demand deposits are part of the money supply (they thought fractional reserve banking was only pernicious to notes). As a result, country banks could still issue deposit certificates.
15. In July 1845 Peel's act is imposed also in Scotland, bringing Scottish banks under BoE's suzerainty and ending free banking there.
16. Inflationary booms and busts continue. In times of trouble the BoE gets Parliament to suspend Peel's act (in 1847, 1857, 1866, and 1914) so that it can issue new notes (to save other banks) without these notes being backed up. The final remains of Peel's Act are scrapped in 1928.

