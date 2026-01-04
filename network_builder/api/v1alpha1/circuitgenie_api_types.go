/*
Copyright 2025.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package v1alpha1

// EndpointSpec define the desired state of Site-to-Site link
type EndpointSpec struct {
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"portlibraries"}`
	// +eda:ui:orderpriority=100
	Port string `json:"port"`
	// +kubebuilder:validation:Optional
	// +eda:ui:autocomplete=`{"group":"core.eda.nokia.com", "version":"v1", "resource":"toponodes"}`
	// +eda:ui:orderpriority=200
	// +eda:ui:title="Node"
	// +eda:ui:visibleif=`self.advanced ===true`
	Node string `json:"node"`
	// +kubebuilder:validation:Optional
	// +eda:ui:orderpriority=300
	// +eda:ui:title="IP Address"
	// +eda:ui:visibleif=`self.advanced ===true`
	IPAddress string `json:"ipAddress,omitempty"`
}

// CircuitGenieSpec defines the desired state of CircuitGenie
type CircuitGenieSpec struct {
	// +eda:ui:display="table"
	// +eda:ui:addButtonText="Add Endpoint"
	Endpoints []EndpointSpec `json:"endpoints"`
	// +kubebuilder:validation:Required
	// +eda:ui:orderpriority=200
	// +eda:ui:columnspan=2
	// +eda:ui:title="Supernet"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"subnetgenies"}`
	Supernet []string `json:"supernet,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:orderpriority=300
	// +eda:ui:columnspan=3
	// +eda:ui:title="Subnet"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"subnetlibraries"}`
	Subnets []string `json:"subnets,omitempty"`
}

// CircuitGenieStatus defines the observed state of CircuitGenie
type CircuitGenieStatus struct{}
