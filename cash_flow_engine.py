from typing import List, Dict, Optional

class Indicator:
    """
    Represents a financial indicator with a canonical ID, a display name,
    and a list of aliases (synonyms) in any language.
    """
    def __init__(self, id: str, display_name: str, aliases: List[str]):
        self.id = id
        self.display_name = display_name
        # Normalize aliases to lowercase for case-insensitive matching
        self.aliases = [a.lower().strip() for a in aliases]

class FinancialCalculator:
    def __init__(self):
        self.data: Dict[str, float] = {}  # Stores {canonical_id: value}
        self.registry: Dict[str, Indicator] = {} # Stores {canonical_id: Indicator}
        self.alias_map: Dict[str, str] = {} # Stores {alias: canonical_id} for fast lookup
        
        self._initialize_registry()

    def _initialize_registry(self):
        """
        Defines the standard dictionary of indicators and their aliases.
        """
        # Helper to register items easily
        def reg(id, name, aliases):
            ind = Indicator(id, name, aliases)
            self.registry[id] = ind
            # Map canonical ID to itself as well
            self.alias_map[id.lower()] = id
            # Map display name
            self.alias_map[name.lower()] = id
            # Map all aliases
            for alias in ind.aliases:
                self.alias_map[alias] = id

        # --- Main Components ---
        reg("OperationalCF", "Операционный денежный поток",
        ["delOperationalCF", "OCF", "delOCF", "Operational Cash Flow"])

        reg("InvestingCF", "Инвестиционный денежный поток",
        ["delInvestingCF", "ICF", "delICF", "Investing Cash Flow"])

        reg("FinancingCF", "Финансовый денежный поток",
        ["delFinancingCF", "FCF", "delFCF", "Financing Cash Flow"])

        reg("Cash", "Денежные средства",
        ["delCash", "C", "delC", "Cash"])

        # --- Components needs to define
        reg("assets", "Активы",
        ["delAssets", "A", "delA", "Assets"])

        reg("liabilities", "Обязательства",
        ["delLiabilities", "L", "delL", "Liabilities"])

        reg("equity", "Собственный капитал",
        ["delEquity", "E", "delE", "Equity"])

        reg("retained_earnings", "Накопленная прибыль",
        ["delRetainedEarnings", "RE", "delRE", "Retained Earnings"])

        reg("current_assets", "Оборотные активы",
        ["delCurrentAssets", "CA", "delCA", "Current Assets"])

        reg("non_current_assets", "Внеоборотные активы",
        ["delNonCurrentAssets", "NCA", "delNCA", "Non-Current Assets"])

        # Other components
        reg("contributed_capital", "Акционерный капитал",
        ["delContributedCapital", "CC", "delCC", "Contributed Capital"])

        reg("other_equity", "Прочий собственный капитал",
        ["delOtherEquity", "OE", "delOE", "Other Equity", "other_equity"])

        reg("non-current liabilities", "Долгосрочные обязательства",
        ["delNonCurrentLiabilities", "NCL", "delNCL", "Non-Current Liabilities", "non-current_liabilities"])

        reg("net_income", "Чистая прибыль",
        ["delNetIncome", "NI", "Net Income", "net income"])

        reg("dividends", "Дивиденды",
        ["delDividends", "Div", "delDiv", "Dividends"])

        reg("net_accounts_receivable", "Дебиторская задолженность (за вычетом резерва по сомнительным долгам и прочих резервов)",
        ["delNetAccountsReceivable", "NetA/R", "delNetA/R", "Net Accounts Receivable", "net accounts receivable"])

        reg("inventory", "Товарно-материальные запасы",
        ["delInventory", "Inv", "delInv", "Inventory"])

        reg("other_current_assets", "Прочие оборотные активы",
        ["delOtherCurrentAssets", "OCA", "delOCA", "Other Current Assets"])

        reg("net_property, plant & equipment", "Основные средства (за вычетом накопленной амортизации)",
        ["delNetPropertyPlantEquipment", "NetPPE", "delNetPPE", "Net Property Plant Equipment", "net property plant equipment"])

        reg("other_non_current_assets", "Прочие внеборотные активы",
        ["delOtherNonCurrentAssets", "ONCA", "delONCA", "Other Non-Current Assets"])

        reg("depreciation_expence", "Амортизация",
        ["delDepreciationExpence", "DE", "delDE", "DepExp", "Depreciation Expence", "depreciation_expence"])

        reg("gain_loss_on_disposal_of_PPE", "Прибыль (убыток) от реализации объектов основных средств",
        ["delGainLossOnDisposalOfPPE", "GLODOPPE", "Gain(Loss)", "delGain(Loss)", "Gain Loss On Disposal Of PPE", "gain loss on disposal of ppe"])

    def resolve_name(self, name: str) -> Optional[str]:
        """
        Finds the canonical ID for a given name (alias).
        Returns None if not found.
        """
        return self.alias_map.get(name.lower().strip())

    def set_value(self, name: str, value: float):
        """
        Sets a value for an indicator using any of its aliases.
        """
        canonical_id = self.resolve_name(name)
        if not canonical_id:
            raise ValueError(f"Unknown indicator name: '{name}'")
        
        self.data[canonical_id] = float(value)
        print(f"Set '{self.registry[canonical_id].display_name}' ({canonical_id}) = {value}")

    def get_value(self, name: str) -> float:
        """
        Gets a value using any alias. Returns 0.0 if not set.
        """
        canonical_id = self.resolve_name(name)
        if not canonical_id:
            print(f"Warning: Unknown indicator '{name}', returning 0.0")
            return 0.0
        return self.data.get(canonical_id, 0.0)


    def calculate_operational_cf(self) -> float:
        """
        Formula: OperationCF = Net Income + Depreciation + Gain(Loss) + Net Accounts Receivable - Inventory - Other Current Assets + Current Liabilities - Gain(Loss) on Disposal of PPE
        """
        ni = self.get_value("net_income")
        dep_exp = self.get_value("depreciation_expence")
        net_ar = self.get_value("net_accounts_receivable")
        inv = self.get_value("inventory")
        oca = self.get_value("other_current_assets")
        cl = self.get_value("current_liabilities")
        gain_loss = self.get_value("gain_loss_on_disposal_of_PPE")
        
        total_operation_cf = ni + dep_exp + net_ar - inv - oca + cl - gain_loss
        
        # Store result
        self.data["operation_cf"] = total_operation_cf
        return total_operation_cf

    def calculate_investing_cf(self) -> float:
        """
        Formula: InvestingCF = -Net Property, Plant & Equipment (NPPPE) + Gain(Loss) on Disposal of PPE + Depreciation (DE) - Other Non-Current Assets (ONCA) + Other Equity (OE)
        """
        nppe = self.get_value("net_property_plant_equipment")
        gain_loss = self.get_value("gain_loss_on_disposal_of_PPE")
        dep_exp = self.get_value("depreciation_expence")
        onca = self.get_value("other_non_current_assets")
        oe = self.get_value("other_equity")
        
        total_investing_cf = -nppe + gain_loss + dep_exp - onca + oe
        
        # Store result
        self.data["investing_cf"] = total_investing_cf
        return total_investing_cf

    def calculate_financing_cf(self) -> float:
        """
        Formula: FinancingCF = Non-Current Liabilities (NCL) + Contributed Capital (CC) - Dividends (Div)
        """
        
        ncl = self.get_value("non_current_liabilities")
        cc = self.get_value("contributed_capital")
        div = self.get_value("dividends")
        
        total_financing_cf = ncl + cc - div
        
        # Store result
        self.data["financing_cf"] = total_financing_cf
        return total_financing_cf

    def calculate_cash(self) -> float:
        """
        Formula: Cash = OperationCF + InvestingCF + FinancingCF
        """
        operation_cf = self.get_value("operation_cf")
        investing_cf = self.get_value("investing_cf")
        financing_cf = self.get_value("financing_cf")
        
        total_cash = operation_cf + investing_cf + financing_cf
        
        # Store result
        self.data["cash"] = total_cash
        return total_cash

