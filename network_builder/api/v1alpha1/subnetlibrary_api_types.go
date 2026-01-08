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

// SubnetLibrarySpec defines the desired state of SubnetLibrary
// +eda:ui:condition=`{"condition":"!(spec.nodes.length === 0 && spec.nodeSelector.length === 0)", "errorMsg":"Either nodes or nodeSelector must have at least one value set"}`
type SubnetLibrarySpec struct {
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=2
	// +eda:ui:orderpriority=100
	// +eda:ui:title="Subnet"
	// IPv4 subnet to allocate subnets from, e.g. 10.1.0.0/16
	Subnet string `json:"subnets,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=1
	// +eda:ui:orderpriority=200
	// +eda:ui:title="Subnet Length"
	// The size of the subnets to be allocated from within the parent subnet, e.g. 29 (which could allocate 10.1.0.8/29, for example).
	// +kubebuilder:default=30
	SubnetLength int `json:"subnetLength,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=2
	// +eda:ui:orderpriority=300
	// +eda:ui:title="SuperNet Name"
	SuperNet string `json:"supernet,omitempty"`
	// +eda:ui:title="Used By"
	UsedBy string `json:"usedby,omitempty"`
}

// SubnetLibraryStatus defines the observed state of SubnetLibrary
type SubnetLibraryStatus struct {
	// +eda:ui:title="Used By"
	UsedBy []string `json:"usedby,omitempty"`
}
