from rest_framework import serializers
from .models import Company, FiscalYear, ProfitLossStatement, BalanceSheet

class ProfitLossSerializer(serializers.ModelSerializer):
    net_profit_margin = serializers.SerializerMethodField()

    class Meta:
        model = ProfitLossStatement
        fields = [
            'year_id', 'revenue', 'ebitda', 'operating_profit', 
            'opm_percentage', 'net_profit', 'eps', 'sales_growth',
            'net_profit_margin'
        ]

    def get_net_profit_margin(self, obj):
        if obj.revenue and obj.net_profit and float(obj.revenue) > 0:
            margin = (float(obj.net_profit) / float(obj.revenue)) * 100
            return round(margin, 2)
        return 0.00


class BalanceSheetSerializer(serializers.ModelSerializer):
    debt_to_equity_ratio = serializers.SerializerMethodField()

    class Meta:
        model = BalanceSheet
        fields = [
            'year_id', 'equity_capital', 'reserves', 'borrowings', 
            'other_liabilities', 'total_assets', 'book_value', 'face_value',
            'debt_to_equity_ratio'
        ]

    def get_debt_to_equity_ratio(self, obj):
        total_equity = float(obj.equity_capital or 0) + float(obj.reserves or 0)
        if total_equity > 0 and obj.borrowings is not None:
            ratio = float(obj.borrowings) / total_equity
            return round(ratio, 2)
        return 0.00


class CompanyProfileSerializer(serializers.ModelSerializer):
    income_statements = serializers.SerializerMethodField()
    balance_sheets = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            'symbol', 'company_name', 'sector', 'website', 
            'about_company', 'income_statements', 'balance_sheets'
        ]

    def get_income_statements(self, obj):
        statements = ProfitLossStatement.objects.filter(company=obj).order_by('year_id')
        return ProfitLossSerializer(statements, many=True).data

    def get_balance_sheets(self, obj):
        sheets = BalanceSheet.objects.filter(company=obj).order_by('year_id')
        return BalanceSheetSerializer(sheets, many=True).data