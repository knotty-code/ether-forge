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

// CircuitGenieSpec defines the desired state of CircuitGenie
// +eda:ui:condition=`{"condition":"!(spec.nodes.length === 0 && spec.nodeSelector.length === 0)", "errorMsg":"Either nodes or nodeSelector must have at least one value set"}`
type CircuitGenieSpec struct {
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=3
	// +eda:ui:orderpriority=100
	// +eda:ui:title="Port-B"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"portlibraries"}`
	// Select interface from Port Library.
	PortA []string `json:"portA,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=3
	// +eda:ui:orderpriority=150
	// +eda:ui:title="Port-A"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"portlibraries"}`
	// Select interface from Port Library.
	PortB []string `json:"portB,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=3
	// +eda:ui:orderpriority=200
	// +eda:ui:title="Supernet"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"subnetgenies"}`
	Supernet []string `json:"supernet,omitempty"`
}

// CircuitGenieStatus defines the observed state of CircuitGenie
type CircuitGenieStatus struct {
	// +eda:ui:title="Nodes"
	// List of nodes this banner has been applied to
	Nodes []string `json:"nodes,omitempty"`
	// +eda:ui:title="Subnets"
	Subnets []string `json:"subnets,omitempty"`
}
