/*
Copyright 2026.

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

// CircuitLibrarySpec defines the desired state of CircuitLibrary
// +eda:ui:condition=`{"condition":"!(spec.nodes.length === 0 && spec.nodeSelector.length === 0)", "errorMsg":"Either nodes or nodeSelector must have at least one value set"}`
type CircuitLibrarySpec struct {
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

// CircuitLibraryStatus defines the observed state of CircuitLibrary
type CircuitLibraryStatus struct{}
