import React from 'react';

const CobacRegulations = () => {

    const backToDashboardUrl = '/dashboard'; 
    const regulationsData = [
        {
            title: "COBAC REGULATION MFI R-2017/07",
            subtitle: "RELATING TO THE CLASSIFICATION, RECORDING AND PROVISIONING OF LOANS OF MICROFINANCE INSTITUTIONS",
            articles: [
                {
                    art: "R-2017/07 ART. 1",
                    text: "Article 1- Microfinance Institutions shall classify record and provision loans held by clients and any counterparty under the conditions provided for in the Chart of Accounts of Microfinance Institutions (PCEMF) and this Regulation."
                },
                {
                    chapter: "CHAPTER 1 - DEFINITIONS"
                },
                {
                    art: "R-2017/07 ART. 2",
                    text: "Article 2- Microfinance Institutions shall classify their loan portfolio as \"performing\" and \"non-performing\" loans. The classification of loans in the appropriate categories shall be carried out independently of the guarantees held."
                },
                {
                    art: "R-2017/07 ART. 3",
                    text: (
                        <>
                            Article 3- For the purposes of this Regulation, the term "loan" shall refer to all commitments on the balance sheet and off-balance sheet held by a Microfinance Institution to counterparty (natural person or legal entity) in the form of:
                            <ul className="list-disc space-y-1 ml-8 mt-2">
                                <li>credits by disbursement or advances, regardless of their nature, form and term;</li>
                                <li>irrevocable commitments by signature (such as guarantees, endorsements, acceptances, irrevocable financing commitments, etc.) in favour of another party;</li>
                                <li>debt securities issued by the other party and held by the institution;</li>
                                <li>leasing on movable and immovable property.</li>
                            </ul>
                            A Counterparty shall be any natural person or legal entity who receives disbursement loans or commitments by signature from a microfinance institution or issuer of debt securities held by such an institution.
                        </>
                    )
                },
                {
                    art: "R-2017/07 ART. 4",
                    text: "Article 4 - Performing loans shall refer to loans whose repayment is made in accordance with the contractual provisions and which are held on other parties whose ability to honor all their current and future commitments raises no reason for concern (solid financial situation, quality shareholding, satisfactory situation and outlook of the business sector, etc.). The expected and immature values accepted by the drawee and whose good end does not raise doubts shall also be considered as performing loans."
                },
                {
                    art: "R-2017/07 ART. 5",
                    text: "Article 5 - Non-performing loans shall consist of \"State-owed defaulted loans\", \"unpaid loans\" and \"bad loans\"."
                },
                {
                    art: "R-2017/07 ART. 6",
                    text: "Article 6 - State-owed defaulted loans are direct claims on the State or guaranteed by the State, advances on public contracts entered in the State budget and pledged and whose payments are irrevocably held in the books of the Microfinance Institution, and advances on securities issued by the State, which have been due for more than 45 days but whose final repayment, without being compromised, cannot be made immediately by the State or the secured debtor"
                },
                {
                    art: "R-2017/07 ART. 7",
                    text: (
                        <>
                            Article 7- Unpaid loans shall be amounts not paid at the contractual maturity. They include:
                            <ul className="list-disc space-y-1 ml-8 mt-2">
                                <li>loan maturities other than that of immovable property unpaid for a period less than or equal to 45 days;</li>
                                <li>rents for simple leases, leases with the option to purchase or immovable property leasing and unpaid mortgages for a period less than or equal to 90 days;</li>
                                <li>rents for simple lease, lease with option to purchase or lease on movable property, unpaid for a period less than or equal to 45 days;</li>
                                <li>overruns of authorized credit limits (amount and/or period of validity) recorded on the current accounts, which are not regularized within a period less than or equal to 45 days;</li>
                                <li>interest and/or principal of overdue and unpaid debt obligations for a term less than or equal to 45 days.</li>
                            </ul>
                            Also considered as unpaid shall be loans that have been forfeited for less than 45 days for any reason other than the occurrence of unpaid debts or the debtor's inability to repay.
                        </>
                    )
                },
                {
                    art: "R-2017/07 ART. 8",
                    text: (
                        <>
                            Article 8 - Doubtful loans shall be claims of any kind which present a probable risk of total or partial non-recovery, even if accompanied by a guarantee. They comprise notably:
                            <ul className="list-disc space-y-1 ml-8 mt-2">
                                <li>loans other than those for immovable property with at least one unpaid instalment for more than 45 days;</li>
                                <li>outstanding mortgage loans with at least one unpaid instalment for more than 90 days;</li>
                                <li>outstanding simple lease operations, lease with option to purchase or lease related to immovable property with at least a rent unpaid for more than 90 days;</li>
                                <li>outstanding operating leases, lease with purchase options or leases on movable assets with unpaid rent for more than 45 days;</li>
                                <li>debit balance of current or ordinary accounts debit balances with no significant credit movement for more than 45 days;</li>
                                <li>current or ordinary account debit balances above the authorized credit limits (amount and/or period of validity), not settled for more than 45 days;</li>
                                <li>claims of a contentious nature ( loans which have been the subject of judicial recovery, of a collective action brought against the debtor - preventive settlement, judicial adjustment, liquidation of assets, personal bankruptcy - loans giving rise to disputed recovery or arbitration proceedings, termination of the leasing contract);</li>
                                <li>debt securities due but unpaid for more than 45 days. The following shall also be considered as doubtful loans:</li>
                                <li>loans that have defaulted for more than 45 days, other than those referred to in article 7;</li>
                                <li>irrevocable commitments by signature, in favour of other parties which present a probable or certain risk of partial or total default or whose loans are classified as doubtful.</li>
                            </ul>
                        </>
                    )
                },
                {
                    art: "R-2017/07 ART. 9",
                    text: "Article 9 - The classification of doubtful loans of a part of the loans carried by another party shall entail the transfer of the totality of the loans held on this counterpart into doubtful outstanding loans, notwithstanding any consideration related to the guarantees possibly held (contagion effect or spill over effect). Irrecoverable non-performing loans shall also include loans on groups or persons related to the other party concerned, considered as the same beneficiary, as stipulated in article 7 of COBAC Regulation EMF-2002/08 of 13 April 2002, relating to the spreading of risks of Microfinance Institutions. The Banking Commission may extend the scope of the related persons in view of the objective elements in its possession and inform the institution concerned."
                },
                {
                    art: "R-2017/07 ART. 10",
                    text: "Article 10 - Bad loans shall be the loans whose non-recovery is ascertained after all amicable or judicial actions and means have been exhausted, or for any other relevant consideration. Doubtful loans that have been fully provisioned for more than 3 years must be written off as bad debts, subject to the provisions of article 25 of this Regulation."
                },
                {
                    art: "R-2017/07 ART. 11",
                    text: "Article11- Consolidated amounts shall be amounts of restructured or rescheduled debts, as negotiated between the institution and its client."
                },
                {
                    chapter: "CHAPTER 2 - PROCESSING OF RESTRUCTURED LOANS"
                },
                {
                    art: "R-2017/07 ART. 12",
                    text: "Article 12- The provisions of this Chapter shall apply to loans whose initial contractual terms are subject to amendments or renewal by new agreements because of the financial situation of the borrower, or by the extension of their duration (rescheduled loans), or by renegotiating all of their initial conditions (restructured loans)."
                },
                {
                    art: "R-2017/07 ART. 13",
                    text: "Article 13- A microfinance institution shall agree on new repayment terms with a client or a member whose loans are classified as unpaid loans, State-owed defaulted loans or doubtful loans. With the exception of the Board of Directors, the body that authorizes the restructuring or rescheduling operation must be in a hierarchically superior position to that of the person or body that originally authorized the loan. However, such loans may only be rescheduled or restructured upon the express decision of the competent body of the microfinance institution, which shall ensure that the financial situation of the borrower makes it possible to repay the debt under the new conditions."
                },
                {
                    art: "R-2017/07 ART. 14",
                    text: (
                        <>
                            Article 14 - The reclassification of a restructured or rescheduled overdue loan into performing loans may only occur if:
                            <ul className="list-disc space-y-1 ml-8 mt-2">
                                <li>the other party makes a repayment equal to at least the greater of the following amounts:
                                    <ul className="list-[circle] space-y-1 ml-8">
                                        <li>i. 20% of the amount of the loan settled after negotiation;</li>
                                        <li>ii. total interest accrued included in the original receivable prior to negotiation;</li>
                                    </ul>
                                </li>
                                <li>the repayment is financed by the other party's own funds. It must not be the subject of direct financing by the microfinance institution or financing of the microfinance institution for persons considered as the same beneficiary as the said counterpart within the meaning of Article 7 of COBAC Regulation EMF-2002/08 of 13 April 2002 on the division of risks.</li>
                            </ul>
                            Otherwise, the loan is maintained in its initial classification category for a period of 90 days, starting from the first maturity of the consolidation loan. Its reclassification among performing loans can only occur at the end of this transitional period, provided that no unpaid instalment is registered during this period. Provisions made prior to restructuring or rescheduling may only be brought forward at the end of the transitional period. With the exception of State-owed defaulted loans, any unpaid instalment during the transitional period shall lead to the automatic decommissioning of the outstanding instalment of the restructured or rescheduled loan. The loan initially classified as doubtful shall remain in this category when an unpaid instalment occurs during the transitional period and must also be fully provisioned. The loan initially classified as State-owed defaulted loan shall remain in this category in the event of an unpaid instalment during the transitional period.
                        </>
                    )
                },
                {
                    chapter: "CHAPTER 3 - TERMS AND CONDITIONS OF CLASSIFICATION AND RECORDING OF CLAIMS"
                },
                {
                    art: "R-2017/07 ART. 15",
                    text: (
                        <>
                            Article 15 – Overdue debts and bad debts shall be recorded in accordance with the following principles:
                            <ol className="list-[lower-alpha] list-inside space-y-1 ml-8 mt-2">
                                <li>State-owed defaulted loans and unpaid claims must be identified in specific accounts provided for by the Chart of Accounts of MFI.</li>
                                <li>unpaid balances noticed will be cleared, in order of occurrence, as and when paid; in any event, if the oldest of the arrears charged to the same debtor is older than 45 days or 90 days as the case may be, they will be subject to the treatment reserved for doubtful debts.</li>
                                <li>loans that have become doubtful shall be taken out of their original account and charged to the "doubtful debts" account for each class.</li>
                                <li>interest and commissions due shall be recorded in the revenue accounts only if they are actually collected, as follows:
                                    <ul className="list-disc list-inside space-y-1 ml-8">
                                        <li>the accounting entries for interests and commissions recorded before the reclassification as State-owed defaulted loans, unpaid loans or doubtful debts are reversed if the products concerned have not actually been collected; these products are then recorded in off-balance sheet accounts;</li>
                                        <li>Interest generated on State-owed defaulted loans long-term, unpaid loans and doubtful debts shall not be recognized in the revenue accounts; they shall be recorded in off-balance sheet accounts.</li>
                                    </ul>
                                </li>
                                <li>Bad debts must be written off for the full amount. The totality of the provisions previously constituted on these loans will have to be brought forward.</li>
                                <li>Doubtful commitments by signature shall be tracked in the "doubtful commitments" account of class 9.</li>
                                <li>Pending compliance with the provisions of Article 14 of this Regulation are complied with, the consolidated amounts shall be monitored, in accordance with the duration of the consolidation, in the main accounts "long-term credits" "medium-term credits" and "short-term credits" "within fractional accounts" moratorium or consolidated credits on the State "with regard to the State and “non-allocable credits" for the other customers.</li>
                            </ol>
                        </>
                    )
                },
                {
                    chapter: "Chapter 4- PROVISIONING RULES"
                },
                {
                    art: "R-2017/07 ART. 16",
                    text: "Article 16 - Microfinance institutions shall constitute provisions for the coverage of doubtful loans."
                },
                {
                    art: "R-2017/07 ART. 17",
                    text: (
                        <>
                            Article 17 - Provisions for doubtful or non-performing loans shall be constituted in accordance with the following principles.
                            <ol className="list-decimal list-inside space-y-1 ml-8 mt-2">
                                <li>The provision is optional for State-owed defaulted loans, unpaid loans and doubtful debts on the State or guaranteed by the State.</li>
                                <li>The provisioning of doubtful debts not covered by the State guarantee is carried out as follows:
                                    <ul className="list-[lower-alpha] list-inside space-y-1 ml-8">
                                        <li>claims which are fully covered by one of the eligible guarantees provided for in Article 17 (1) and (2) below shall not give rise to any provisioning;</li>
                                        <li>claims fully covered by one of the eligible guarantees provided for in sub- paragraphs 3, 4 and 5 of Article 18 of this Regulation shall have been fully provisioned within a maximum of four years. The accumulated provision must cover: at least 25% of the total gross risks concerned at the end of the first year, 50% at the end of the second year, 75% at the end of the third year and 100% at the end of the fourth year;</li>
                                        <li>loans not covered by one of the eligible guarantees provided for in Article 17 of this Regulation must be fully provisioned within a maximum of one year;</li>
                                        <li>loans shall partially be covered by one of the eligible guarantees provided for in Article 18 of this Regulation shall be provisioned in accordance with the provisions of (c) above, up to the amount not covered by the guarantee.</li>
                                    </ul>
                                </li>
                            </ol>
                            The amount of specific provisions is obtained by multiplying the gross outstanding amount of each receivable by the applicable provisioning rate. Provisions shall be recorded no later than the annual closing date following the declassification into doubtful debts, in accordance with the terms of rates set in point 2-b of the first paragraph. Doubtful loans relating to leasing and renting operations with purchase option shall be provisioned to the tune of their amount. The processing provided for in this article shall be applicable to all loans recorded in the balance sheet, regardless of when they were set up or decommissioned as doubtful loans.
                        </>
                    )
                },
                {
                    art: "R-2017/07 ART. 18",
                    text: (
                        <>
                            Article 18 - The eligible guarantees referred to in Article 16 above are:
                            <ol className="list-decimal list-inside space-y-1 ml-8 mt-2">
                                <li>cash transfers and cash pledges (security deposits, term accounts or cash vouchers subscribed from the institution concerned itself, or negotiable debt securities);</li>
                                <li>pledge of debt securities issued by the State;</li>
                                <li>counter-guarantees received from a credit institution set up in CEMAC;</li>
                                <li>guarantees received from multilateral development banks, multilateral guarantee agencies, or public financing or guarantee agencies established in CEMAC;</li>
                                <li>real sureties: mortgages, commissaria lex, etc.</li>
                            </ol>
                        </>
                    )
                },
                {
                    art: "R-2017/07 ART. 19",
                    text: (
                        <>
                            Article 19 - For it to be considered, pursuant to the provisions of Article 16 above, the guarantees shall:
                            <ul className="list-disc space-y-1 ml-8 mt-2">
                                <li>be put in writing and recorded in accordance with the legal and regulatory provisions in force;</li>
                                <li>expressly state that these values are used to cover the risks incurred;</li>
                                <li>have a maturity at least equal to that of the hedged credit or hedged signature commitment;</li>
                                <li>be stipulated at first request, in the case of counter-guarantees received from a credit institution.</li>
                            </ul>
                        </>
                    )
                },
                {
                    art: "R-2017/07 ART. 20",
                    text: "Article 20- Doubtful debts relating to leasing and rental operations with purchase options shall be provisioned, in both corporate accounting and cost accounting, on the basis of their respective amounts in these two accounts. These loans shall be provisioned in accordance with the provisions of Article 17 (b) above."
                },
                {
                    art: "R-2017/07 ART. 21",
                    text: "Article 21- Eligible mortgages are first or second grade firm mortgages on buildings. These mortgages shall be duly drawn up and registered."
                },
                {
                    art: "R-2017/07 ART. 22",
                    text: "Article 22 - The specific provisions are recorded in the accounts provided for this purpose in the appropriate classes of the Chart of accounts of microfinance institutions. In particular, the provisions relating to bad debts on leasing are recorded in the \"provisions for bad debts on leasing\" account. Provisions relating to commitments by doubtful signature are recorded, as the case may be, in the \"provisions for the execution of guarantee and caution commitments\" account, or, in the case of commitments relating to leasing or renting with option to purchase, in provisions for risk of non-collection of rents” account. The provisions necessary to cover the risk of loss are determined and must be recorded, at the latest, on the date of closing of the annual financial statements."
                },
                {
                    art: "R-2017/07 ART. 23",
                    text: "Article 23 - The identification of State-owed defaulted loans, unpaid claims and doubtful debts is abandoned when the payments resume regularly for the amounts corresponding to the deadlines and if the arrears are cleared."
                },
                {
                    art: "R-2017/07 ART. 24",
                    text: "Article 24 - The Banking Commission may, where it deems justified, require claims against another party to be classified in a given category and covered by appropriate provisions."
                },
                {
                    art: "R-2017/07 ART. 25",
                    text: "Article 25 - The rules laid down in this Regulation for the classification of claims in one or the other category of outstanding receivables and their provisioning shall constitute minimum obligations to be respected by the institutions subject to this Regulation."
                },
                {
                    art: "R-2017/07 ART. 26",
                    text: "Article 26 - The prior approval of the Secretary General of the Banking Commission is required for any loss or waiver of debts owed to groups or related parties. Related parties include subsidiaries of the institution, affiliated companies and any party (including its subsidiaries, affiliates and ad hoc structures) over which the microfinance institution exercises control or which exercises control over it. It may also include the principal shareholders, directors, general management, personnel, their direct or indirect interests, their relatives, as well as corresponding persons in the affiliated institutions"
                },
                {
                    art: "R-2017/07 ART. 27",
                    text: "Article 27 - Subjected institutions must periodically declare to the Banking Commission the status of their commitments, in accordance with the terms and conditions set by the Banking Commission."
                },
                {
                    chapter: "CHAPTER 5: FINAL PROVISIONS"
                },
                {
                    art: "R-2017/07 ART. 28",
                    text: "Article 28- The CEMAC microfinance institutions operating on the date of entry into force of this Regulation shall have a transitional period of twenty-four (24) months maximum, to comply with the provisions of the Regulation."
                },
                {
                    art: "R-2017/07 ART. 29",
                    text: "Article 29- In the event of non-compliance with the provisions of this Regulation, the measures provided for by the regulations in force shall apply."
                },
                {
                    art: "R-2017/07 ART. 30",
                    text: "Article 30- This Regulation repeals all previous provisions which are contrary to it, in particular COBAC Regulation EMF 2002/18 on the recording and provisioning of bad debts."
                },
                {
                    art: "R-2017/07 ART. 31",
                    text: "Article 31- All previous provisions repugnant to this regulation are hereby repealed."
                },
                {
                    art: "R-2017/07 ART. 32",
                    text: "Article 32- This Regulation shall enter into force on 1 January 2018."
                },
                {
                    art: "R-2017/07 ART. 33",
                    text: "Article 33- The Secretary General of COBAC shall be charged with the application of this Regulation and its notification to the National Monetary Authorities, to the National Head Offices of the Bank of Central African States, to the professional Associations of Credit Institutions and the professional Associations of Microfinance Institutions of the Central African Economic and Monetary Community."
                },
            ]
        },
        {
            title: "COBAC REGULATION MFI R-2017/08",
            subtitle: "SETTING THE CAP ON LOAN GRANTING BY MICROFINANCE INSTITUTIONS.",
            articles: [
                {
                    art: "R-2017/08 ART. 1",
                    text: "Article 1- This Regulation sets the maximum amount of loan that a Microfinance Institution shall grant to one of its clients /members."
                },
                {
                    art: "R-2017/08 ART. 2",
                    text: "Article 2- Subject to the provisions of paragraph 2, the maximum amount of loan a Microfinance Institution, irrespective of its category, may grant to one of its members or clients shall be capped at 10% of its paid-up capital. The maximum amount of loan a Microfinance Institution, irrespective of its category, may grant to one of its shareholders or cooperative members, Board members, the Executive or staff shall be capped at CFA francs 50 million. The above caps are set, without prejudice to the obligation of Microfinance Institutions, to comply with other risk-related prudential standards laid down by regulations in force."
                },
                {
                    art: "R-2017/08 ART. 3",
                    text: "Article 3- The loan amount referred to in article 2 above shall mean all commitments in cash and by signature"
                },
                {
                    art: "R-2017/08 ART. 4",
                    text: "Article 4- Loans granted before the entry into force of this Regulation shall not be taken into account for its application."
                },
                {
                    art: "R-2017/08 ART. 5",
                    text: "Article 5 In case of non-compliance with the provisions herein, the measures stipulated by the regulations in force shall be applicable."
                },
                {
                    art: "R-2017/08 ART. 6",
                    text: "Article 6- All previous provisions repugnant to this regulation are hereby repealed."
                },
                {
                    art: "R-2017/08 ART. 7",
                    text: "Article 7- This regulation enters into force with effect from 1 July 2018."
                },
            ]
        }
    ];

    return (
        <div className="max-w-4xl mx-auto p-6 mt-10 sm:p-8 bg-white rounded-3xl shadow-2xl space-y-8 border border-slate-200 text-slate-900">

            {/* Page Title Section */}
            <div className="text-center pb-4 border-b-2 border-indigo-400">
                <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 leading-tight">
                    COBAC Regulations
                </h2>
                <p className="mt-2 text-lg text-slate-600">
                    Key guidelines for loan granting and portfolio management.
                </p>
            </div>

            {/* COBAC Regulations Section */}
            <div className="bg-slate-50 p-6 rounded-xl shadow-md border border-slate-200 overflow-y-auto max-h-[600px] md:max-h-[700px]">
                <h3 className="text-2xl font-bold text-slate-800 mb-4 border-b border-slate-300 pb-2">COBAC Regulations</h3>
                
                {/* Dynamically render the two main regulations */}
                {regulationsData.map((reg, regIndex) => (
                    <div key={regIndex} className="mt-8">
                        <p className="text-sm text-slate-600 mb-4">
                            <strong className='font-bold'>{reg.title}</strong><br />
                            {reg.subtitle}
                        </p>

                        {/* Render all articles for the current regulation */}
                        {reg.articles.map((item, itemIndex) => (
                            <div key={itemIndex}>
                                {item.chapter ? (
                                    <h4 className="text-lg font-semibold text-slate-800 mb-2 mt-4 text-center border-t border-slate-300 pt-2">
                                        {item.chapter}
                                    </h4>
                                ) : (
                                    <p className="mb-4 text-slate-700">
                                        <strong className='font-bold'>{item.art}</strong><br />
                                        {item.text}
                                    </p>
                                )}
                            </div>
                        ))}
                    </div>
                ))}
                
            </div>
            
            {/* Back to Main Dashboard Link */}
            <div className="mt-8 text-center">
                <a href={backToDashboardUrl} className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-xl shadow-sm text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 ease-in-out">
                    ← Back to Main Dashboard
                </a>
            </div>

        </div>
    );
};

export default CobacRegulations;