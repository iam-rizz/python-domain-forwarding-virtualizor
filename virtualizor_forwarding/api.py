"""
Virtualizor API client.

Handles all communication with the Virtualizor API.
"""

from __future__ import annotations

from typing import Dict, List, Any, Optional
import requests
from urllib3.exceptions import InsecureRequestWarning

from .models import (
    HostProfile,
    VMInfo,
    ForwardingRule,
    HAProxyConfig,
    APIResponse,
)

# Suppress SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class APIError(Exception):
    """API related errors."""

    pass


class ConnectionError(APIError):
    """Connection related errors."""

    pass


class AuthenticationError(APIError):
    """Authentication related errors."""

    pass


class VirtualizorClient:
    """Client for Virtualizor API communication."""

    DEFAULT_TIMEOUT = 30

    def __init__(self, host_profile: HostProfile) -> None:
        """
        Initialize client with host profile.

        Args:
            host_profile: HostProfile containing API credentials.
        """
        self._profile = host_profile
        self._base_url = host_profile.api_url
        self._api_key = host_profile.api_key
        self._api_pass = host_profile.get_decoded_pass()

    def _build_url(self, action: str, **params: Any) -> str:
        """Build API URL with parameters."""
        base_params = {
            "act": action,
            "api": "json",
            "apikey": self._api_key,
            "apipass": self._api_pass,
        }
        base_params.update(params)

        query = "&".join(f"{k}={v}" for k, v in base_params.items())
        return f"{self._base_url}?{query}"

    def _request(
        self,
        action: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        **params: Any,
    ) -> Dict[str, Any]:
        """
        Make API request.

        Args:
            action: API action name.
            method: HTTP method (GET or POST).
            data: POST data if applicable.
            **params: Additional URL parameters.

        Returns:
            JSON response as dictionary.

        Raises:
            ConnectionError: If connection fails.
            AuthenticationError: If authentication fails.
            APIError: For other API errors.
        """
        url = self._build_url(action, **params)

        try:
            if method.upper() == "POST":
                response = requests.post(
                    url,
                    data=data,
                    timeout=self.DEFAULT_TIMEOUT,
                    verify=False,  # Allow self-signed certificates
                )
            else:
                response = requests.get(url, timeout=self.DEFAULT_TIMEOUT, verify=False)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            raise ConnectionError(
                "Connection timeout. Please check:\n"
                "  - Network connectivity\n"
                "  - API URL is correct\n"
                "  - Server is responding"
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Failed to connect to API:\n"
                f"  URL: {self._base_url}\n"
                f"  Error: {e}\n"
                "Please verify the API URL and network connectivity."
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError(
                    "Authentication failed. Please verify:\n"
                    "  - API Key is correct\n"
                    "  - API Password is correct"
                )
            raise APIError(f"HTTP error: {e}")
        except requests.exceptions.JSONDecodeError:
            raise APIError("Invalid JSON response from API")
        except Exception as e:
            raise APIError(f"API request failed: {e}")

    def test_connection(self) -> bool:
        """
        Test API connection and credentials.

        Returns:
            True if connection successful.

        Raises:
            ConnectionError: If connection fails.
            AuthenticationError: If authentication fails.
        """
        try:
            response = self._request("listvs")
            # Check if we got valid response
            return "vs" in response or "error" not in response
        except (ConnectionError, AuthenticationError):
            raise
        except Exception as e:
            raise ConnectionError(f"Connection test failed: {e}")

    def list_vms(self) -> List[VMInfo]:
        """
        Retrieve list of all VMs from server.

        Returns:
            List of VMInfo objects.

        Raises:
            APIError: If API call fails.
        """
        response = self._request("listvs")

        vs_data = response.get("vs", {})
        if not vs_data:
            return []

        vms = []
        for vpsid, vm_data in vs_data.items():
            try:
                vm = VMInfo.from_api_response(vpsid, vm_data)
                vms.append(vm)
            except Exception:
                continue

        return vms

    def get_forwarding(self, vpsid: str) -> List[ForwardingRule]:
        """
        Get forwarding rules for specific VM.

        Args:
            vpsid: VM ID.

        Returns:
            List of ForwardingRule objects.
        """
        response = self._request("managevdf", svs=vpsid)

        haproxy_data = response.get("haproxydata", {})
        if not haproxy_data:
            return []

        rules = []
        for rule_data in haproxy_data.values():
            try:
                rule = ForwardingRule.from_api_response(rule_data)
                rules.append(rule)
            except Exception:
                continue

        return rules

    def add_forwarding(self, vpsid: str, rule: ForwardingRule) -> APIResponse:
        """
        Add new forwarding rule.

        Args:
            vpsid: VM ID.
            rule: ForwardingRule to add.

        Returns:
            APIResponse with result.
        """
        data = {
            "vdf_action": "addvdf",
            "protocol": rule.protocol.value,
            "src_hostname": rule.src_hostname,
            "src_port": str(rule.src_port),
            "dest_ip": rule.dest_ip,
            "dest_port": str(rule.dest_port),
        }

        response = self._request("managevdf", method="POST", data=data, svs=vpsid)
        return APIResponse.from_response(response)

    def edit_forwarding(
        self, vpsid: str, vdfid: str, rule: ForwardingRule
    ) -> APIResponse:
        """
        Edit existing forwarding rule.

        Args:
            vpsid: VM ID.
            vdfid: Forwarding rule ID.
            rule: Updated ForwardingRule.

        Returns:
            APIResponse with result.
        """
        data = {
            "vdf_action": "editvdf",
            "vdfid": vdfid,
            "protocol": rule.protocol.value,
            "src_hostname": rule.src_hostname,
            "src_port": str(rule.src_port),
            "dest_ip": rule.dest_ip,
            "dest_port": str(rule.dest_port),
        }

        response = self._request("managevdf", method="POST", data=data, svs=vpsid)
        return APIResponse.from_response(response)

    def delete_forwarding(self, vpsid: str, vdfids: List[str]) -> APIResponse:
        """
        Delete forwarding rules.

        Args:
            vpsid: VM ID.
            vdfids: List of forwarding rule IDs to delete.

        Returns:
            APIResponse with result.
        """
        data = {
            "vdf_action": "delvdf",
            "ids": ",".join(vdfids),
        }

        response = self._request("managevdf", method="POST", data=data, svs=vpsid)
        return APIResponse.from_response(response)

    def get_server_config(self, vpsid: str) -> HAProxyConfig:
        """
        Get HAProxy configuration for port validation.

        Args:
            vpsid: VM ID.

        Returns:
            HAProxyConfig object.
        """
        response = self._request("managevdf", svs=vpsid, novnc="6710", do="add")
        return HAProxyConfig.from_api_response(response)

    def get_vm_internal_ip(self, vpsid: str) -> Optional[str]:
        """
        Get internal IPv4 address of VM.

        Args:
            vpsid: VM ID.

        Returns:
            IPv4 address string or None.
        """
        vms = self.list_vms()
        for vm in vms:
            if vm.vpsid == str(vpsid):
                return vm.ipv4
        return None
